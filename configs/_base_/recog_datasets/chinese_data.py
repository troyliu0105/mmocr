dataset_type = 'OCRDataset'

root = 'data/chi/Chinese_dataset'
img_prefix = f'{root}/images'
train_anno_file = f'{root}/labels.txt'

train = dict(
    type=dataset_type,
    img_prefix=img_prefix,
    ann_file=train_anno_file,
    loader=dict(
        type='HardDiskLoader',
        repeat=1,
        parser=dict(
            type='LineStrParser',
            keys=['filename', 'text'],
            keys_idx=[0, 1],
            separator=' ')),
    pipeline=None,
    test_mode=False)

train_list = [train]
