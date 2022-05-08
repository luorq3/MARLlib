from ray import tune
from ray.tune.utils import merge_dicts
from ray.tune import CLIReporter
from marl.algos.core.VD.facmac import FACMACRNNTrainer as FACMACTrainer


def run_facmac(config_dict, common_config, env_dict, stop):
    train_batch_size = config_dict["algo_args"]["batch_episode"] * env_dict["episode_limit"]
    episode_limit = env_dict["episode_limit"]
    algorithm = config_dict["algorithm"]
    batch_mode = config_dict["algo_args"]["batch_mode"]
    lr = config_dict["algo_args"]["lr"]

    config = {
        "batch_mode": batch_mode,
        "buffer_size": 5000,
        "train_batch_size": 1000,
        "critic_lr": lr,
        "actor_lr": lr,
        "n_step": 10,
        "model": {
            "max_seq_len": episode_limit,
            "custom_model_config": merge_dicts(config_dict, env_dict),
        },
        "prioritized_replay": True,
        "zero_init_states": True

    }
    config.update(common_config)

    results = tune.run(FACMACTrainer, name=algorithm + "_" + config_dict["model_arch_args"]["core_arch"] + "_" +
                                         config_dict["env_args"][
                                             "map_name"],
                       stop=stop,
                       config=config,
                       verbose=1,
                       progress_reporter=CLIReporter())

    return results
