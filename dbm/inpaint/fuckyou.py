from pylearn2.config import yaml_parse

yaml = """!obj:pylearn2.train.Train {
    dataset: &train !obj:pylearn2.datasets.norb_small.FoveatedNORB {
        which_set: "train",
        scale: 1,
        restrict_instances: [4, 6, 7, 8],
        one_hot: 1
    },
    model: !obj:galatea.dbm.inpaint.super_dbm.SuperDBM {
        inference_procedure: !obj:galatea.dbm.inpaint.super_dbm.BiasInit {},
              batch_size : 100,
              niter: 2, # 14 failed
              visible_layer: &vis !obj:galatea.dbm.inpaint.super_dbm.GaussianVisLayer {
                nvis: 8976,
                bias_from_marginals: *train,
                init_beta: !obj:pylearn2.models.mlp.beta_from_features { dataset: *train , min_var: .01 }
              },
              hidden_layers: [
                !obj:galatea.dbm.inpaint.super_dbm.DenseMaxPool { # BVMP_Gaussian {
                    center: 0,
                    # input_layer: *vis,
                        max_col_norm: .15,
                        detector_layer_dim: 2,
                        pool_size: 1,
                        irange: .001,
                        layer_name: 'h0'
               },
              #  !obj:galatea.dbm.inpaint.super_dbm.DenseMaxPool {
              #      center: 0,
              #          max_col_norm: 2.666304,
              #          detector_layer_dim: 2,
              #          pool_size: 1,
              #          irange: .05,
              #          layer_name: 'h1',
              #          init_bias: -0.393587
              # },
               !obj:galatea.dbm.inpaint.super_dbm.DenseMaxPool {
                    center: 0,
                        max_col_norm: 2.666304,
                        detector_layer_dim: 2,
                        pool_size: 1,
                        irange: .05,
                        layer_name: 'h2',
                        init_bias: -0.393587
               },
               #!obj:galatea.dbm.inpaint.super_dbm.Softmax {
               #     center: 0,
               #         max_col_norm: 5.175683,
               #         irange: .05,
               #         layer_name: 'c',
               #         n_classes: 5
               #}
              ]
    },
    algorithm: !obj:pylearn2.training_algorithms.sgd.SGD {
        #monitoring_dataset : {
        #   'valid': !obj:pylearn2.datasets.norb_small.FoveatedNORB {
             #   which_set: "train",
             #   scale: 1,
             #   restrict_instances: [9],
             #   one_hot: 1
       #     },
           # 'test': !obj:pylearn2.datasets.norb_small.FoveatedNORB {
           #     which_set: "test",
           #     scale: 1,
           #     one_hot: 1
           #  }
        #},
        learning_rate: 2.,
        init_momentum: .5,
        cost: !obj:pylearn2.costs.cost.SumOfCosts {
           costs :[
                       !obj:galatea.dbm.inpaint.super_inpaint.SuperInpaint {
                          # monitor_multi_inference: 1,
                          both_directions: 0,
                          noise: 0,
                           #supervised: 1,
                           mask_gen: !obj:galatea.dbm.inpaint.super_inpaint.MaskGen {
                               drop_prob: 0.02,
                               drop_prob_y: 0.5,
                               balance: 0,
                               sync_channels: 0
                            }
                       }
                       ]
               },
               # termination_criterion: !obj:pylearn2.termination_criteria.MonitorBased
               # {
               #          channel_name: "valid_err",
               #          N: 100,
               #          prop_decrease: 0.
               # }
        },
    extensions: [
                !obj:pylearn2.training_algorithms.sgd.MomentumAdjustor {
                    start: 1,
                    saturate: 2,
                    final_momentum: 0.732716
                },
                !obj:pylearn2.training_algorithms.sgd.LinearDecayOverEpoch {
                    start: 1,
                    saturate: 868,
                    decay_factor: 0.020379
                }
        ],
    save_freq : 1
}
"""

train_obj = yaml_parse.load(yaml)

train_obj.main_loop()
