from __future__ import annotations

import ray
from ray.rllib.agents import ppo
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.policy.policy import PolicySpec
from ray.tune.logger import pretty_print
from Chess_Agent_RL.Models.Action_Mask_Model import ActionMaskModel
from Chess_Agent_RL.Game.Chess import Game

agent_id_conversion = {'white': 0, 'black': 1}


class SelfPlayCallback(DefaultCallbacks):
    def __init__(self):
        super().__init__()

    def on_train_result(self, *, algorithm, result, **kwargs):
            # Set the weights of the opponent's policy to the main policy
            main_state = algorithm.get_policy("chess_agent").get_state()
            algorithm.get_policy("opponent").set_state(main_state)
            # We need to sync the just copied local weights (from main policy)
            # to all the remote workers as well.
            algorithm.workers.sync_weights()


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
                    "opponent": PolicySpec()},
                policy_mapping_fn=lambda agent_id, episode, worker, **kwargs:
                'chess_agent' if episode.episode_id % 2 == agent_id_conversion[agent_id] else 'opponent',
                policies_to_train=["chess_agent"], )
            .resources(num_gpus=num_gpus)
            .rollouts(num_rollout_workers=0)
        )

        self.algo = self.config.build()


    def training(self, stop_iters: int = 10):
        ray.shutdown()
        ray.init(num_cpus=self.num_cpus)
        # run manual training loop and print results after each iteration
        for i in range(stop_iters):
            result = self.algo.train()
            print(pretty_print(result))
            if (i + 1) % 100 == 0:
                self.algo.save(f"model_checkpoint_{i}")

        ray.shutdown()

    @classmethod
    def restore(cls, path: str) -> PPOAgent:
        ppo_agent = cls()
        ppo_agent.algo.restore(path)
        return ppo_agent


if __name__ == '__main__':
    agent = PPOAgent()
    agent.training(5)
