import subprocess
import argparse


def sim_cpma_pipeline(input_folder, samplesize):
    targets = [ 0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    beta_values = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1]
    
    metaconfig_cmd = f'python write_metaconfig.py -i {input_folder} -s {samplesize}'.split(' ')
    #subprocess.call(metaconfig_cmd)
    print('Finished writing metaconfig files')

    print('Starting generating config files')
    configen_cmd = []
    for tar in targets:
        for beta in beta_values:
            value = str(beta).replace(".","")
            configen_cmd.append(f'python config_generator_specific.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -i 100 -o {input_folder}/numTarget_{tar}/Beta_{value}'.split(' '))
    configen_procs = [ subprocess.Popen(i) for i in configen_cmd]
    for p in configen_procs:
        p.wait()
    print('Finished generating config files')

    print('Starting simulations')
    simulate_cmd = []
    for tar in targets:
        for beta in beta_values:
            value = str(beta).replace(".","")
            simulate_cmd.append(f'python simulate_expression_givenoise.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -i 100 -o {input_folder}/numTarget_{tar}/Beta_{value}'.split(' '))
    simulate_procs = [ subprocess.Popen(i) for i in simulate_cmd]
    for p in simulate_procs:
        p.wait()
    print('Finished simulating files')

    print('Starting running cpma pipeline')
    cpma_cmd = []
    for tar in targets:
        for beta in beta_values:
            value = str(beta).replace(".","")
            cpma_cmd.append(f'python ../CPMA/run_cpma_pipeline_sim.py -f {input_folder}/numTarget_{tar}/Beta_{value} -i 100'.split(' '))
    cpma_procs = [ subprocess.Popen(i) for i in cpma_cmd]
    for p in cpma_procs:
        p.wait()
    print('Finished calculating cpma') 
   
    print('Starting comparing to chi distribution')
    chidist_cmd = []
    for tar in targets:
        for beta in beta_values:
            value = str(beta).replace(".","")
            chidist_cmd.append(f'python compute_pvalue_chidist.py -i {input_folder}/numTarget_{tar}/Beta_{value} -t 1 -n 100'.split(' '))
    chidist_procs = [ subprocess.Popen(i) for i in chidist_cmd]
    for p in chidist_procs:
        p.wait()
    print('Finished comparing to chi distribution')

    print('Starting to calculate power')
    power_cmd = []
    for tar in targets:
        for beta in beta_values:
            value = str(beta).replace(".","")
            power_cmd.append(f'python calculate_power_singleqtl_cpma.py -c {input_folder}/numTarget_{tar}/Beta_{value}/metaconfig.yaml -f {input_folder}/numTarget_{tar}/Beta_{value} -i 100'.split(' '))
    power_procs = [ subprocess.Popen(i) for i in power_cmd]
    for p in power_procs:
        p.wait()
    print('Finished calculating power')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder", required=True, help="Input folder with num_target and Beta folders")
    parser.add_argument("-s", "--samplesize", type=int, default=0, help="Sample size")
    params = parser.parse_args()

    sim_cpma_pipeline(input_folder=params.input_folder,
          samplesize=params.samplesize)


if __name__ == "__main__":
    main()