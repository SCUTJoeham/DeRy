_base_ = [
    '../../_base_/datasets/cifar100_bs128.py',
    '../../_base_/schedules/cifar100_bs256.py',
    '../../_base_/default_runtime.py',
]

model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='TIMMBackbone',
        model_name='vit_small_patch16_224',
        pretrained=True),
    neck=None,
    head=dict(
        type='LinearClsHead',
        num_classes=100,
        in_channels=384,
        loss=dict(
            type='LabelSmoothLoss',
            label_smooth_val=0.1,
            num_classes=100,
            reduction='mean',
            loss_weight=1.0),
        topk=(1, 5)),
)


            
