#!/usr/bin/env python
from dcgan import *
from madgan import *
from began import *
from wgan import *
from gogan import *
from modegan import *
from unrolledgan import *
from magan import *
from infogan import *
from madgan_ind import *
from models.toy_models import *
from models.toy_models_ind import *
from eval_funcs import eval_synthetic
import random
from datasets.data_synthetic import *

if __name__ == '__main__':
    args = parse_args(lr=1e-4, #TODO
                      additional_args=[('--n_gen', {'type': int, 'default': 0}),]) #TODO n_gen
    print args

    if args.gpu:
        set_gpu(args.gpu)

    # Random seed set
    random.seed(4)

    # Network params
    dim_x = 1  #2 TODO
    dim_h = 128
    dim_z = 64
    dim_ae = 32     # BEGAN only
    n_categorical = 5 #InfoGAN only TODOi
    n_generators = args.n_gen   # MADGAN only

    # Training params
    params = {'n_iters': 200000, 'batch_size': args.batchsize, 'lr': args.lr, 'dim_z': dim_z} #TODO n_iters

    #Output storage
    stat_entries = {}
    prob = [1, 0.05, 0.1, 0.2]
    lpf = [1, 1, 1, 1] #lowerProbFactor
    hpf = [1, 20, 10, 5] #higherProbFactor

    #for name, data in [('SynMoG', rect_MoG(5)),('SynSpiral', Spiral())]:
    #for name, data in [('SynMoG_1', rect_MoG(5))]:
    #for name, data in [('SynMoG_'+str(prob[iteri]), rect_MoG(5, lpf[iteri], hpf[iteri]))]
    #for name, data in [('SynMoG_1', specs_MoG(5, 1, 1, 0.25))]
    #for name, data in [('specs_gen1_'+str(iteri), specs_MoG1D(5))]: #TODO for dim_x = 1
    #for name, data in [('rect_gen1_'+str(iteri), rect_MoG(5))]:
    #for name, data in [('specs_gen1_'+str(iteri), specs_MoG1D_20mod(20,1,1,2))]:
    
    for iteri in range(1):
        n_generators = 4
        for name, data in [('specs_gen1_'+str(iteri), specs_MoG1D(5))]:
            print('Iteration is ' + str(iteri))
            # Evaluation func.
            gen_eval_func = lambda tag, batch_size: \
                lambda it, sample_generator: eval_synthetic(it, sample_generator, data, tag=tag, batch_size=batch_size)

            # Common generator
#            g_net = ToyNet(dim_x, dim_z, dim_h=dim_h, last_act=tf.identity, act=tf.nn.elu, bn=False)
            #params['batch_size'] = n_generators * int(128 / n_generators)   #batch_size is multiple of generators, TODO Comment it out

            # Disc. for DCGAN (sigmoid)
#            d_net = ToyNet(1, dim_x, dim_h=dim_h, last_act=tf.sigmoid, act=leaky_relu, bn=False)
#            train_dcgan(data, g_net, d_net, name='DCGAN_' + name,
#                        eval_funcs=[gen_eval_func('DCGAN_' + name, params['batch_size'])],
#                        **params)
#
#            # InfoGAN
#            d_net = ToyNetInd(1, dim_x, dim_h=dim_h, last_act=tf.sigmoid, act=leaky_relu, bn=False)
#            g_infonet = ToyNet(dim_x, dim_z+n_categorical, dim_h=dim_h, last_act=tf.identity, act=tf.nn.elu, bn=False)
#            train_infogan(data, g_infonet, d_net, name='InfoGAN_' + name, n_categorical=n_categorical,
#                        eval_funcs=[gen_eval_func('InfoGAN_' + name, params['batch_size'])],
#                        **params)
            


            # Disc. for MADGAN (multi-output)
            g_net_ind = ToyNetInd(dim_x, dim_z, dim_h=dim_h, last_act=tf.identity, act=tf.nn.elu, bn=False)
            d_net = ToyNetInd(n_generators + 1, dim_x, dim_h=dim_h, last_act=tf.identity, act=leaky_relu, bn=False)
            train_madgan_ind(data, g_net_ind, d_net, name='MADGAN_ind_' + name, n_generators=n_generators,
                        eval_funcs=[gen_eval_func('MADGAN_ind_' + name, params['batch_size'])],
                        **params)
            
            # Disc. for MADGAN (multi-output)
            n_generators = 5
            params['batch_size'] = n_generators * int(128 / n_generators) 
            d_net = ToyNet(n_generators + 1, dim_x, dim_h=dim_h, last_act=tf.identity, act=leaky_relu, bn=False)
            train_madgan(data, g_net_ind, d_net, name='MADGAN_' + name, n_generators=n_generators,
                        eval_funcs=[gen_eval_func('MADGAN_' + name, params['batch_size'])],
                        **params)
#
#            # Disc. for WGAN and GoGAN (identity)
#            d_net = ToyNet(1, dim_x, dim_h=dim_h, last_act=tf.identity, act=leaky_relu, bn=False)
#            train_wgan(data, g_net, d_net, name='WGAN_' + name,
#                       eval_funcs=[gen_eval_func('WGAN_' + name, params['batch_size'])],
#                       **params)
#            train_gogan(data, g_net, d_net, name='GoGAN_' + name,
#                       eval_funcs=[gen_eval_func('GoGAN_' + name, params['batch_size'])],
#                       **params)
#
#            # Encoder-decoder for BEGAN
#            d_enc = ToyNet(dim_ae, dim_x, dim_h=dim_h, last_act=tf.identity, act=leaky_relu, bn=False)
#            d_dec = ToyNet(dim_x, dim_ae, dim_h=dim_h, last_act=tf.identity, act=tf.nn.elu, bn=False)
#
#            train_began(data, g_net, d_enc, d_dec, name='BEGAN_' + name,
#                        eval_funcs=[gen_eval_func('BEGAN_' + name, params['batch_size'])],
#                        **params)
#
#
#            d_enc = ToyNet(dim_z, dim_x, dim_h=dim_h, last_act=tf.identity, act=leaky_relu, bn=False)
#            d_net = ToyNet(1, dim_x, dim_h=dim_h, last_act=tf.sigmoid, act=leaky_relu, bn=False)
#            train_modegan(data, g_net,d_enc, d_net, name='MODEGAN_' + name,
#                        eval_funcs=[gen_eval_func('MODEGAN_' + name, params['batch_size'])],
#                        **params)
#
#
#            # Disc. for MAGAN
#            d_net = ToyNet(1, dim_x, dim_h=dim_h, last_act=tf.sigmoid, act=leaky_relu, bn=False)
#            train_trivial(data, g_net, d_net, name='TRIVIAL_' + name, n_generators=n_generators,
#                         eval_funcs=[gen_eval_func('TRIVIAL_' + name, params['batch_size'])],
#                         **params)
#
#            d_net = ToyNet(1, dim_x, dim_h=dim_h, last_act=tf.sigmoid, act=leaky_relu, bn=False)
#            train_UNROLLEDGAN(data, g_net, d_net, name='UNROLLEDGAN_' + name,
#                        eval_funcs=[gen_eval_func('UNROLLEDGAN_' + name, params['batch_size'])],
#                        **params)
