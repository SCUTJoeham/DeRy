_base_ = [
    '../../_base_/datasets/cifar100_bs128.py',
    '../../_base_/schedules/cifar100_bs256.py',
    '../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='SwinTransformer', arch='small', img_size=224,
        drop_path_rate=0.3,
        init_cfg=dict(
            type='Pretrained',
            checkpoint='https://download.openmmlab.com/mmclassification/v0/swin-transformer/swin_small_224_b16x64_300e_imagenet_20210615_110219-7f9d988b.pth',
            prefix='backbone',
        )),
    neck=dict(type='GlobalAveragePooling'),
    head=dict(
        type='LinearClsHead',
        num_classes=100,
        in_channels=768,
        init_cfg=None,  # suppress the default init_cfg of LinearClsHead.
        loss=dict(
            type='LabelSmoothLoss', label_smooth_val=0.1, mode='original'),
        cal_acc=False),
    init_cfg=[
        dict(type='TruncNormal', layer='Linear', std=0.02, bias=0.),
        dict(type='Constant', layer='LayerNorm', val=1., bias=0.)
    ],
    # train_cfg=dict(augments=[
    #     dict(type='BatchMixup', alpha=0.8, num_classes=100, prob=0.5),
    #     dict(type='BatchCutMix', alpha=1.0, num_classes=100, prob=0.5)
    # ])
)



            
