_base_ = [
    '../../_base_/datasets/airplane_bs256_2.py',
    '../../_base_/schedules/downstream_bs256_adamw.py',
    '../../_base_/default_runtime.py',
]

# Input shape: (3, 224, 224)
# Flops: 1.89 GFLOPs
# Params: 3.34 M
# My Params: 3.33522M
optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=5e-4 * 256 / 512,
    weight_decay=0.05,
    eps=1e-8,
    betas=(0.9, 0.999),
    paramwise_cfg=dict(norm_decay_mult=0., bypass_duplicate=True))

fp16 = dict(loss_scale=512.0)
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='DeRy',
        block_fixed=True,
        base_channels=64,
        block_list=[dict(model_name='swsl_resnext50_32x4d',
                         block_input='layer1.0',
                         block_output='layer1.2',
                         backend='mytimm'),
                    dict(model_name='swsl_resnext50_32x4d',
                         block_input='layer2.0',
                         block_output='layer2.0',
                         backend='mytimm'),
                    dict(model_name='regnet_y_800mf',
                         block_input='trunk_output.block3.block3-3',
                         block_output='trunk_output.block3.block3-7',
                         backend='pytorch'),
                    dict(model_name='vit_tiny_patch16_224',
                         block_input='blocks.11',
                         block_output='blocks.11',
                         backend='mytimm')
                    ],
        adapter_list=[
            dict(
                input_channel=256,
                output_channel=256,
                stride=1,
                num_fc=0,
                num_conv=1,
                mode='cnn2cnn'),
            dict(
                input_channel=512,
                output_channel=320,
                stride=2,
                num_fc=0,
                num_conv=1,
                mode='cnn2cnn'),
            dict(
                input_channel=320,
                output_channel=192,
                num_fc=0,
                stride=1,
                num_conv=1,
                mode='cnn2vit')
        ],
        out_indices=(3, )),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes={{_base_.dataset_num_classes}},
        in_channels=192,
        loss=dict(
            type='LabelSmoothLoss',
            label_smooth_val=0.1,
            num_classes={{_base_.dataset_num_classes}},
            reduction='mean',
            loss_weight=1.0),
        topk=(1, 5),
        cal_acc=False),
    train_cfg=dict(augments=[
        dict(type='BatchMixup', alpha=0.1,
             num_classes={{_base_.dataset_num_classes}}, prob=0.5),
        dict(type='BatchCutMix', alpha=1.0,
             num_classes={{_base_.dataset_num_classes}}, prob=0.5)
    ])
)

# evaluation = dict(interval=2000, metric='accuracy')
evaluation = dict(interval=2000, metric='per_class_acc')
checkpoint_config = dict(interval=2000, max_keep_ckpts=2)