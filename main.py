import src.configuration.config_utils as config_utils
import os
import argparse


def process_command_line():
    parser = argparse.ArgumentParser(description='usage')
    parser.add_argument('--config', dest='config', type=str, default='config.yaml', 
                        help='config file for this experiment')
    args = parser.parse_args()
    return args
 

if __name__ == '__main__':
    args = process_command_line()

    experiment_configs = config_utils.get_experiment_configs(args.config)

    for config in experiment_configs:
        os.makedirs(config.working_dir)
        config_utils.write_config(
            config=config,
            path=os.path.join(config.working_dir, 'config.yaml'))


