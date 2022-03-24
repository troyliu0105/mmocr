dataset_type = 'OCRDataset'

img_prefix_scsd = 'data/chi/Synthetic_Chinese_String_Dataset/images'
train_anno_file_scsd = 'data/chi/Synthetic_Chinese_String_Dataset/scsd_train.txt'
val_anno_file_scsd = 'data/chi/Synthetic_Chinese_String_Dataset/scsd_test.txt'

train_scsd = dict(
    type=dataset_type,
    img_prefix=img_prefix_scsd,
    ann_file=train_anno_file_scsd,
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

val_scsd = dict(
    type=dataset_type,
    img_prefix=img_prefix_scsd,
    ann_file=val_anno_file_scsd,
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

img_prefix_chi = 'data/chi/Chinese_dataset/images'
train_anno_file_chi = 'data/chi/Chinese_dataset/labels.txt'

train_chi = dict(
    type=dataset_type,
    img_prefix=img_prefix_chi,
    ann_file=train_anno_file_chi,
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

train_list = [train_scsd, train_chi]
test_list = [val_scsd]
