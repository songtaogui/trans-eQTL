import argparse
import numpy as np
from numpy import linalg as LA
from scipy.stats import norm
import math


def calculate_cpma(sim_pvalues, num_genes):
    likelihood = np.mean(np.negative(np.log(sim_pvalues)))
    value = -2 * ((((likelihood - 1) * num_genes)/likelihood) - num_genes*np.log(likelihood))
    return value


def simulateZscores(zfile, efile, qfile, output, n):
    #mean_zscores = np.loadtxt('/storage/cynthiawu/trans_eQTL/Nerve-Tibial/chr1_gene_snp_eqtls_meanzscores.csv', dtype=complex, delimiter='\t')
    mean_zscores = np.loadtxt(zfile, delimiter='\t')
    print('mean zscores file read')
    #print(mean_zscores.shape)

    #e_values = np.loadtxt('/storage/cynthiawu/trans_eQTL/Nerve-Tibial/chr1_gene_snp_eqtls_evalues.csv', dtype=complex, delimiter='\t')
    e_values = np.loadtxt(efile, dtype=complex, delimiter='\t')
    n_genes = len(e_values)
    print(n_genes)
    print('e_values file read')
    #Q = np.loadtxt('/storage/cynthiawu/trans_eQTL/Nerve-Tibial/chr1_gene_snp_eqtls_Q.csv', dtype=complex, delimiter='\t')
    Q = (np.loadtxt(qfile, dtype=complex, delimiter='\t')).real
    print('Q file read')
    diag_e_values = np.diag(e_values)
    E = (np.sqrt(diag_e_values)).real
    #print(E)
    
    print('starting simulations')
    #print(Q.shape)
    #print(E.shape)
    e_matrix = np.dot(Q, E)
   
    sim_cpma = []
    iterations = math.ceil(n/1000)
    #print(iterations)
    sim_undone = n
    #perform in chunks of 1000
    for i in range(iterations):
        cur_n = min(1000, sim_undone)
        sim_undone = sim_undone - cur_n
        print(n-sim_undone)

        z=np.random.normal(0, 1, (cur_n, n_genes))
        #print(z.shape)
        mzscores_tile = np.tile(mean_zscores, (cur_n, 1))
        #print(mzscores_tile.shape)
        sim_zscores = mzscores_tile + np.dot(z, e_matrix)
        #print(sim_zscores.shape)
        sim_pvalues = norm.cdf(sim_zscores)
        #print(sim_pvalues.shape)
        for sim in sim_pvalues:
            cpma = calculate_cpma(sim, n_genes)
            sim_cpma.append(cpma)

    print('simuated cpma calculated')

    sim_cpma = np.array(sim_cpma)
   # np.savetxt('/storage/cynthiawu/trans_eQTL/Nerve-Tibial/chr1_gene_snp_eqtls_simzscores100.csv', sim_zscores, delimiter='\t')
    np.savetxt(output, sim_cpma, delimiter='\t', fmt='%f')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--mzscores", required=True, help="Input mean zscores file")
    parser.add_argument("-e", "--eigenvalues", required=True, help="Input eigenvalues file")
    parser.add_argument("-q", "--eigenvectors", required=True, help="Input eigenvectorsfile")
    parser.add_argument("-o", "--output", required=True, help="Ouptput file with simulated cpma values")
    parser.add_argument("-n", "--simulations", required=True, type=int, help="Number of simulations")
    params = parser.parse_args()
    np.random.seed(0)
    simulateZscores(params.mzscores, params.eigenvalues, params.eigenvectors, params.output, params.simulations)


if __name__ == "__main__":
    main()
