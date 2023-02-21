from __future__ import annotations

import ray
from ray.rllib.agents import ppo
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.policy.policy import PolicySpec
from ray.tune.logger import pretty_print
from Chess_Agent_RL.Models.Action_Mask_Model import ActionMaskModel
from Chess_Agent_RL.Game.Chess import Game
import numpy as np

agent_id_conversion = {'white': 0, 'black': 1}


class SelfPlayCallback(DefaultCallbacks):
    def __init__(self):
        super().__init__()
        # 0=RandomPolicy, 1=1st main policy snapshot,
        # 2=2nd main policy snapshot, etc..
        self.current_opponent = 0
        self.win_rate_threshold = 0.5

    def on_train_result(self, *, algorithm, result, **kwargs):
        # Get the win rate for the train batch.
        # Note that normally, one should set up a proper evaluation config,
        # such that evaluation always happens on the already updated policy,
        # instead of on the already used train_batch.
        main_rew = result["hist_stats"].pop("policy_chess_agent_reward")
        #TODO: Add evaluation config and use results of that
        won = 0
        for r_main in main_rew:
            if r_main == 100:
                won += 1
        win_rate = won / len(main_rew)
        result["win_rate"] = win_rate
        print(f"Iter={algorithm.iteration} win-rate={win_rate} -> ", end="")
        # If win rate is good -> Snapshot current policy and play against
        # it next, keeping the snapshot fixed and only improving the "main"
        # policy.
        if win_rate > self.win_rate_threshold:
            self.current_opponent += 1
            new_pol_id = f"main_v{self.current_opponent}"

            # Re-define the mapping function, such that "main" is forced
            # to play against any of the previously played policies
            # (excluding "random").
            def policy_mapping_fn(agent_id, episode, worker, **kwargs):
                # agent_id = [0|1] -> policy depends on episode ID
                # This way, we make sure that both policies sometimes play
                # (start player) and sometimes agent1 (player to move 2nd).
                return (
                    "chess_agent"
                    if episode.episode_id % 2 == agent_id_conversion[agent_id]
                    else "main_v{}".format(
                        np.random.choice(list(range(1, self.current_opponent + 1)))
                    )
                )

            new_policy = algorithm.add_policy(
                policy_id=new_pol_id,
                policy_cls=type(algorithm.get_policy("chess_agent")),
                policy_mapping_fn=policy_mapping_fn,
            )

            # Set the weights of the new policy to the main policy.
            # We'll keep training the main policy, whereas `new_pol_id` will
            # remain fixed.
            main_state = algorithm.get_policy("chess_agent").get_state()
            new_policy.set_state(main_state)
            # We need to sync the just copied local weights (from main policy)
            # to all the remote workers as well.
            algorithm.workers.sync_weights()

        # +2 = main + random
        result["league_size"] = self.current_opponent + 2


class PPOAgent:
    def __init__(self, num_gpus: float = 0.75, num_cpus: int | None = None, eager_tracing: bool = True):
        self.num_cpus = num_cpus

        self.config = (
            ppo.PPOConfig()
            .environment(Game, disable_env_checking=True)
            .framework('tf2', eager_tracing=eager_tracing)
            .callbacks(SelfPlayCallback)
            .training(model={"custom_model": ActionMaskModel})
            .multi_agent(
                policies={
                    "chess_agent": PolicySpec(),
                    "random": PolicySpec()},
                policy_mapping_fn=lambda agent_id, episode, worker, **kwargs:
                'chess_agent' if episode.episode_id % 2 == agent_id_conversion[agent_id] else 'random',
                policies_to_train=["chess_agent"], )
            .resources(num_gpus=num_gpus)
            .rollouts(num_rollout_workers=0)
        )

        self.algo = self.config.build()


    def training(self, stop_iters: int = 10, stop_timesteps: int = 10000000000000000000000):
        ray.shutdown()
        ray.init(num_cpus=self.num_cpus)
        # run manual training loop and print results after each iteration
        for i in range(stop_iters):
            result = self.algo.train()
            print(pretty_print(result))
            # stop training if the target train steps or reward are reached
            #if result["timesteps_total"] >= stop_timesteps:
            #    break
            if (i + 1) % 100 == 0:
                self.algo.save(f"model_checkpoint_{i}")

        ray.shutdown()

    @classmethod
    def restore(cls, path: str) -> PPOAgent:
        agent = cls()
        agent.algo.restore(path)
        return agent

    def compute_single_action(self, state:dict):
        move, _, _ = self.algo.get_policy('chess_agent').compute_single_action(state, explore=False)
        return move


if __name__ == '__main__':
    agent = PPOAgent()
    agent.training(5)
