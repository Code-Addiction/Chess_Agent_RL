import tensorflow as tf

from gym.spaces import Dict

from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.tf.tf_modelv2 import TFModelV2


class ActionMaskModel(TFModelV2):
    def __init__(
        self, obs_space, action_space, num_outputs, model_config, name, **kwargs
    ):

        orig_space = getattr(obs_space, "original_space", obs_space)
        assert (
            isinstance(orig_space, Dict)
            and "action_mask" in orig_space.spaces
            and "state" in orig_space.spaces
        )

        super().__init__(obs_space, action_space, num_outputs, model_config, name)

        self.internal_model = FullyConnectedNetwork(
            orig_space["state"],
            action_space,
            num_outputs,
            model_config,
            name + "_internal",
        )

    def forward(self, input_dict, state, seq_lens):
        #print("input_dict:", input_dict)
        #print("state:", state)
        #print("seq_lens:", seq_lens)
        # Extract the available actions tensor from the observation.
        action_mask = input_dict["obs"]["action_mask"]
        #print("action_mask:", action_mask)

        # Compute the unmasked logits.
        logits, _ = self.internal_model({"obs": input_dict["obs"]["state"]})
        #print("logits:", logits)

        # Convert action_mask into a [0.0 || -inf]-type mask.
        inf_mask = tf.maximum(tf.math.log(action_mask), tf.float32.min)
        #print("inf_mask:", inf_mask)

        masked_logits = logits + inf_mask
        #print("masked_logits:", masked_logits)

        # Return masked logits.
        return masked_logits, state

    def value_function(self):
        return self.internal_model.value_function()

    def import_from_h5(self, h5_file: str) -> None:
        pass
