from models import CustomResponse, Status
from anuvaad_auditor.loghandler import log_info, log_exception
from utilities import MODULE_CONTEXT
import os
import json
import sys
import re
import utilities.sentencepiece_util as sp
import utilities.fairseq_sentence_processor as sentence_processor
import config
import datetime
from services import load_models


class FairseqDocumentTranslateService:
    @staticmethod
    def batch_translator(input_dict):

        model_id = input_dict["id"]
        src_list = input_dict["src_list"]
        num_sentence = len(src_list)
        input_subwords_list = [None] * num_sentence
        output_subwords_list = [None] * num_sentence
        tagged_src_list = [None] * num_sentence
        tagged_tgt_list = [None] * num_sentence
        tgt_list = [None] * num_sentence
        score_list = [None] * num_sentence
        out = {}

        date_original_array = [None] * num_sentence
        url_original_array = [None] * num_sentence
        num_array_array = [None] * num_sentence
        num_map_array = [None] * num_sentence
        prefix_array = [None] * num_sentence

        # sp_encoder, translator, sp_decoder = get_models(model_id)
        translator = load_models.loaded_models[model_id]
        source_bpe = load_models.bpes[model_id][0]
        # target_bpe = load_models.bpes[i["id"]][1]

        input_sentence_array_prepd = [None] * num_sentence
        special_case_sentence_indices = []

        src_language, tgt_language = misc.get_src_tgt_langauge(model_id)

        try:
            for i, sent in enumerate(src_list):
                input_sentence = sent.strip()
                # if src_language == 'English' and input_sentence.isupper():
                #     input_sentence = input_sentence.title()

                # input_sentence = misc.convert_digits_preprocess(src_language,input_sentence)

                # if special_case_handler.special_case_fits(input_sentence):
                #     special_case_sentence_indices.append(i)
                #     log_info(
                #         "sentence fits in special case, capturing index to process at last",
                #         MODULE_CONTEXT,
                #     )
                # else:
                #     (
                #         prefix_array[i],
                #         input_sentence,
                #     ) = special_case_handler.prefix_handler(input_sentence)
                #     (
                #         input_sentence,
                #         date_original_array[i],
                #         url_original_array[i],
                #         num_array_array[i],
                #         num_map_array[i],
                #     ) = tagger_util.tag_number_date_url(input_sentence)
                #     tagged_src_list[i] = (
                #         prefix_array[i] + " " + input_sentence
                #     ).lstrip()

                input_sentence_array_prepd[i] = input_sentence

            # (
            #     input_sentence_array_prepd,
            #     sent_indices_wo_stop,
            # ) = special_case_handler.handle_sentences_wo_stop(
            #     src_language, input_sentence_array_prepd
            # )

            log_info("translating using NMT-model:{}".format(model_id), MODULE_CONTEXT)
            # if model_id == 6:
            #     "hi-en_exp-2 05-05-20"
            #     input_sentence_array_prepd = [
            #         sentence_processor.indic_tokenizer(sentence)
            #         for sentence in input_sentence_array_prepd
            #     ]
            #     (
            #         translation_array,
            #         input_subwords_list,
            #         output_subwords_list,
            #         score_list,
            #     ) = encode_translate_decode(
            #         input_sentence_array_prepd,
            #         sp_encoder,
            #         translator,
            #         sp_decoder,
            #         input_subwords_list,
            #         output_subwords_list,
            #         score_list,
            #     )
            #     translation_array = [
            #         sentence_processor.moses_detokenizer(translation)
            #         for translation in translation_array
            #     ]

            # elif model_id == 56:
            #     "09/12/19-Exp-5.6:"
            #     input_sentence_array_prepd = [
            #         sentence_processor.moses_tokenizer(sentence)
            #         for sentence in input_sentence_array_prepd
            #     ]
            #     (
            #         translation_array,
            #         input_subwords_list,
            #         output_subwords_list,
            #         score_list,
            #     ) = encode_translate_decode(
            #         input_sentence_array_prepd,
            #         sp_encoder,
            #         translator,
            #         sp_decoder,
            #         input_subwords_list,
            #         output_subwords_list,
            #         score_list,
            #     )
            #     translation_array = [
            #         sentence_processor.indic_detokenizer(translation)
            #         for translation in translation_array
            #     ]
            if i["id"] == 100:
                "hindi-english"
                translation_array = encode_translate_decode(
                    input_sentence_array_prepd, "hi", "en", translator, source_bpe
                )
            elif i["id"] == 101:
                "bengali-english"
                translation_array = encode_translate_decode(
                    input_sentence_array_prepd, "bn", "en", translator, source_bpe
                )
            elif i["id"] == 102:
                "tamil-english"
                translation_array = encode_translate_decode(
                    input_sentence_array_prepd, "ta", "en", translator, source_bpe
                )

            else:
                log_info(
                    "Unsupported model id: {} for given input".format(model_id),
                    MODULE_CONTEXT,
                )
                raise Exception(
                    "Unsupported Model ID - id: {} for given input".format(model_id)
                )

            # translation_array = oc.postprocess_sentences_wo_stop(tgt_language, translation_array, sent_indices_wo_stop)

            # for i in range(num_sentence):

            #     if i in special_case_sentence_indices:
            #         log_info("sentence fits in special case, returning output accordingly and not from model",MODULE_CONTEXT)
            #         tgt_list[i] = special_case_handler.handle_special_cases(src_list[i].strip(),model_id)
            #         score_list[i] = 1
            #         input_subwords_list[i],output_subwords_list[i],tagged_tgt_list[i],tagged_src_list[i] = \
            #             "","",tgt_list[i],src_list[i].strip()
            #     else:
            #         translation_array[i] = (prefix_array[i] +" "+translation_array[i]).lstrip()
            #         translation_array[i] = translation_array[i].replace("▁"," ")
            #         translation_array[i] = .regex_pass(translation_array[i],[patterns['p8'],patterns['p9'],patterns['p4'],patterns['p5'],
            #                             patterns['p6'],patterns['p7']])
            #         tagged_tgt_list[i] = translation_array[i]
            #         translation_array[i] = tagger_util.replace_tags_with_original(translation_array[i],\
            #             date_original_array[i],url_original_array[i],num_array_array[i],num_map_array[i])
            #         translation_array[i] = oc.cleaner(tagged_src_list[i],translation_array[i],model_id)
            #         tgt_list[i] = translation_array[i]
            #         log_info("translate_function-experiment-{} output: {}".format(model_id,translation_array[i]),MODULE_CONTEXT)

            #     tgt_list[i] = misc.convert_digits_postprocess(tgt_language,tgt_list[i])

            #     if (not tgt_list[i]) or (tgt_list[i].isspace()):
            #         tgt_list[i] = src_list[i]

            # out = {
            #     "tagged_src_list": tagged_src_list,
            #     "tagged_tgt_list": tagged_tgt_list,
            #     "tgt_list": tgt_list,
            # }
            out = {"translations": translation_array}
        except ServerModelError as e:
            log_exception(
                "ServerModelError error in TRANSLATE_UTIL-translate_func: {} and {}".format(
                    e, sys.exc_info()[0]
                ),
                MODULE_CONTEXT,
                e,
            )
            raise e
        except Exception as e:
            log_exception(
                "Exception caught in NMTTranslateService:batch_translator:%s and %s"
                % (e, sys.exc_info()[0]),
                MODULE_CONTEXT,
                e,
            )
            raise e

        return out


# def get_models(model_id):
#     try:
#         _ ,sp_encoder,sp_decoder = get_model_path(model_id)
#         translator = load_models.loaded_models[model_id]
#         return sp_encoder, translator, sp_decoder
#     except Exception as e:
#         log_exception("Exception caught in document_translate service:get_models: {} ".format(e),MODULE_CONTEXT,e)
#         raise

# def encode_translate_decode(input_sentence_array_prepd,sp_encoder,translator,sp_decoder,input_subwords_list,output_subwords_list,score_list):
#     try:
#         log_info("Inside encode_translate_decode function",MODULE_CONTEXT)
#         input_subwords_list = [str(sp.encode_line(sp_encoder,sent)) for sent in input_sentence_array_prepd]
#         input_final_array = [format_converter(input_subwords) for input_subwords in input_subwords_list]
#         m_out = translator.translate_batch(input_final_array,beam_size = 5,num_hypotheses=1,replace_unknowns=True)
#         translation_array = [None] * len(output_subwords_list)
#         for i, _ in enumerate(output_subwords_list):
#                 output_subwords_list[i] = " ".join(m_out[i][0]['tokens'])
#                 score_list[i] = m_out[i][0]['score']
#                 translation_array[i] = multiple_hypothesis_decoding(m_out[i],sp_decoder)[0]
#         return translation_array, input_subwords_list, output_subwords_list, score_list
#     except ServerModelError as e:
#         log_exception("ServerModelError error in encode_translate_decode: {} and {}".format(e,sys.exc_info()[0]),MODULE_CONTEXT,e)
#         raise

#     except Exception as e:
#         log_exception("Unexpexcted error in encode_translate_decode: {} and {}".format(e,sys.exc_info()[0]),MODULE_CONTEXT,e)
#         raise

# def format_converter(input):
#     inp_1 = input.split(', ')
#     inp_2 = [inpt+',' if inpt != inp_1[-1] else inpt for inpt in inp_1 ]
#     return inp_2

# def get_model_path(model_id):
#     with open(config.ICONFG_FILE) as f:
#         confs = json.load(f)
#         model_root = confs['models_root']
#         models = confs['models']
#         path = [(model["path"],model["sp_encoder"],model["sp_decoder"]) for model in models if model["id"] == model_id]
#         if len(path) == 0:
#             raise Exception("Model id:{} is not valid".format(model_id))
#         final_path =  os.path.join(model_root, path[0][0])
#         s_encoder = os.path.join(model_root, path[0][1])
#         s_decoder = os.path.join(model_root, path[0][2])
#         return final_path,s_encoder,s_decoder

# def multiple_hypothesis_decoding(hypotheses,sp_decoder):
#     try:
#         translations = list()
#         for i in hypotheses:
#             translation = " ".join(i['tokens'])
#             translation = sp.decode_line(sp_decoder,translation)
#             translations.append(translation)
#         return translations
#     except Exception as e:
#         log_exception("Error in interactive translation-multiple_hypothesis_decoding:{}".format(e),MODULE_CONTEXT,e)
#         raise

# def multiple_hypothesis_decoding_v2(hypotheses,sp_decoder):
#     try:
#         translations = list()
#         for i in hypotheses:
#             translation = " ".join(i['tokens'])
#             translation = sp.decode_line_v2(sp_decoder,translation)
#             translations.append(translation)
#         return translations
#     except Exception as e:
#         log_exception("Error in interactive translation-multiple_hypothesis_decoding_v2:{}".format(e),MODULE_CONTEXT,e)
#         raise


def encode_translate_decode(inputs, src_lang, tgt_lang, translator, source_bpe):
    try:
        inputs = sentence_processor.preprocess(inputs, src_lang)
        inputs = apply_bpe(inputs, source_bpe)
        log_info("BPE encoded sent: %s" % inputs, MODULE_CONTEXT)
        i_final = sentence_processor.apply_lang_tags(inputs, src_lang, tgt_lang)
        translation = translator.translate(i_final)
        translation = sentence_processor.postprocess(translation, tgt_lang)
        # log_info("output from model: {}".format(output_sw), MODULE_CONTEXT)
        # scores = m_out[0][0]["score"]
        # translation = multiple_hypothesis_decoding(m_out[0], sp_decoder)[0]
        # log_info("SP decoded sent: %s" % translation, MODULE_CONTEXT)
        # return translation, scores, input_sw, output_sw
        return translation
    except ServerModelError as e:
        log_exception(
            "ServerModelError error in encode_translate_decode: {} and {}".format(
                e, sys.exc_info()[0]
            ),
            MODULE_CONTEXT,
            e,
        )
        raise

    except Exception as e:
        log_exception(
            "Unexpexcted error in encode_translate_decode: {} and {}".format(
                e, sys.exc_info()[0]
            ),
            MODULE_CONTEXT,
            e,
        )
        raise


def apply_bpe(sents, bpe):
    return [bpe.process_line(sent) for sent in sents]