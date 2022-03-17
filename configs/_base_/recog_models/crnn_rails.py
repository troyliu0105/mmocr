label_convertor = dict(
    type='CTCConvertor',
    dict_file='configs/_base_/recog_models/chi_words_3922_dict.txt',
    with_unknown=True,
    lower=False)

model = dict(
    type='CRNNNet',
    preprocessor=None,
    backbone=dict(type='ResNet31OCR',
                  base_channels=1,
                  layers=[1, 2, 3, 2],
                  channels=[64, 128, 256, 256, 512, 512, 512],
                  out_indices=None,
                  stage4_pool_cfg=dict(kernel_size=(8, 1), stride=(8, 1)),
                  last_stage_pool=False,
                  ),
    encoder=None,
    decoder=dict(type='CRNNDecoder', in_channels=512, rnn_flag=True),
    loss=dict(type='CTCLoss'),
    label_convertor=label_convertor,
    max_seq_len=50,
    pretrained=None)
