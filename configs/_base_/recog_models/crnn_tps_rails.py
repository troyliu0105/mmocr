# model
label_convertor = dict(
    type='CTCConvertor',
    dict_file='configs/_base_/recog_models/chi_words_3922_dict.txt',
    with_unknown=True,
    lower=False)

model = dict(
    type='CRNNNet',
    preprocessor=dict(
        type='TPSPreprocessor',
        num_fiducial=20,
        img_size=(32, 100),
        rectified_img_size=(32, 100),
        num_img_channel=1),
    backbone=dict(type='VeryDeepVgg', leaky_relu=False, input_channels=1),
    encoder=None,
    decoder=dict(type='CRNNDecoder', in_channels=512, rnn_flag=True),
    loss=dict(type='CTCLoss'),
    label_convertor=label_convertor,
    pretrained=None)