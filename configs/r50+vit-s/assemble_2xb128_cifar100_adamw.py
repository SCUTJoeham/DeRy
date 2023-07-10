_base_ = [
    '../../_base_/datasets/cifar100_bs128.py',
    '../../_base_/schedules/cifar100_bs256.py',
    '../../_base_/default_runtime.py',
]

model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='DeRy',
        block_fixed=False,
        base_channels=64,
        block_list=[
            ['resnet50', 'layer1.0', 'layer2.1', 'pytorch'],
            ['resnet50', 'layer2.2', 'layer3.4', 'pytorch'],
            ['vit_small_patch16_224', 'blocks.9', 'blocks.10', 'mytimm'],
            ['vit_small_patch16_224', 'blocks.10', 'blocks.11', 'mytimm']
        ],
        adapter_list=[
            dict(
                input_channel=512,
                output_channel=512,
                stride=1,
                num_fc=0,
                num_conv=1,
                mode='cnn2cnn'),
            dict(
                input_channel=1024,
                output_channel=384,
                num_fc=0,
                stride=1,
                num_conv=1,
                mode='cnn2vit'),
            dict(
                input_channel=384,
                output_channel=384,
                num_fc=1,
                num_conv=0,
                mode='vit2vit')
        ],
        out_indices=(3, )),
    neck=dict(type='GlobalAveragePooling'),
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


            
