# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Query an exported model. Py2 only. Install tensorflow-serving-api."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from sacremoses import MosesTruecaser, MosesTokenizer, MosesDetokenizer
from oauth2client.client import GoogleCredentials
from six.moves import input  # pylint: disable=redefined-builtin

from tensor2tensor import problems as problems_lib  # pylint: disable=unused-import
from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
from tensor2tensor.utils.hparam import HParams
import tensorflow as tf

import nltk
import re
from datetime import datetime


mtr = MosesTruecaser('truecase_model/en-truecase.mdl')
mtok = MosesTokenizer()
mdtk = MosesDetokenizer()
sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle') 
pattern = re.compile(r'([\u4e00-\u9fa5, ]{1})\s+([\u4e00-\u9fa5, ]{1})')


flags = tf.flags
FLAGS = flags.FLAGS
#t2t-query-server --t2t_usr_dir=./user_dir --data_dir=./data --problem=translate_enzh_sub32k --servable_name=my_model --server=localhost:8501

flags.DEFINE_string("server", "localhost:8501", "Address to Tensorflow Serving server.")
flags.DEFINE_string("servable_name", "my_model", "Name of served model.")
flags.DEFINE_string("problem", "translate_enzh_sub50k", "Problem name.")
flags.DEFINE_string("data_dir", "./data", "Data directory, for vocab files.")
flags.DEFINE_string("t2t_usr_dir", "./user_dir", "Usr dir for registrations.")
flags.DEFINE_string("inputs_once", None, "Query once with this input.")
flags.DEFINE_integer("timeout_secs", 10, "Timeout for query.")

# For Cloud ML Engine predictions.
flags.DEFINE_string("cloud_mlengine_model_name", None,
                    "Name of model deployed on Cloud ML Engine.")
flags.DEFINE_string(
    "cloud_mlengine_model_version", None,
    "Version of the model to use. If None, requests will be "
    "sent to the default version.")


def validate_flags():
  """Validates flags are set to acceptable values."""
  if FLAGS.cloud_mlengine_model_name:
    assert not FLAGS.server
    assert not FLAGS.servable_name
  else:
    assert FLAGS.server
    assert FLAGS.servable_name


def make_request_fn():
  """Returns a request function."""
  if FLAGS.cloud_mlengine_model_name:
    request_fn = serving_utils.make_cloud_mlengine_request_fn(
        credentials=GoogleCredentials.get_application_default(),
        model_name=FLAGS.cloud_mlengine_model_name,
        version=FLAGS.cloud_mlengine_model_version)
  else:

    request_fn = serving_utils.make_grpc_request_fn(
        servable_name=FLAGS.servable_name,
        server=FLAGS.server,
        timeout_secs=FLAGS.timeout_secs)
  return request_fn

# def translate(_):
tf.logging.set_verbosity(tf.logging.INFO)
# validate_flags()
usr_dir.import_usr_dir(FLAGS.t2t_usr_dir)
problem = registry.problem(FLAGS.problem)
hparams = tf.contrib.training.HParams(
    data_dir=os.path.expanduser(FLAGS.data_dir))
problem.get_hparams(hparams)
request_fn = make_request_fn()


########################################
app = Flask(__name__)
i = 0

class ReviewForm(Form):
    review = TextAreaField("", [validators.DataRequired()])


@app.route('/')
def index():
    # 验证用户输入的文本是否有�?    form = ReviewForm(request.form)
    return render_template("index.html", form=form)


@app.route("/main", methods=["POST"])
def main():
    global i
    i += 1
    form = ReviewForm(request.form)
    if request.method == "POST" and form.validate():
        # 获取表单提交的英�?        inputs = request.form["review"]

        # 获取评论的分类结�?类标、概�?        # Y, lable_Y, proba = classify_review([review_text])
        # 将概率保�?为小数并转换成为百分比的形式
        # proba = float("%.4f" % proba) * 100
        # 将分类结果返回给界面进行显示
        inputs = mtr.truecase((mtok.tokenize(inputs, return_str=True)), return_str=True)
        inputs = sent_tokenizer.tokenize(inputs)
        a = datetime.now()
        outputs = serving_utils.predict(inputs, problem, request_fn)
        outputs = [output for (output, score) in outputs]
        outputs = (''.join(outputs)).replace(' ','')
        #print(outputs)
        b = datetime.now()

        return render_template("index.html", form=form,
                               label=outputs + "�?Time�? + str((b - a).seconds) + "s �?)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')


