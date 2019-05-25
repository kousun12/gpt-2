#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf
import re
import random

import model, sample, encoder
import sample_utils as sf


def interact_model(
        model_name='345M',
        seed=None,
        nsamples=1,
        batch_size=1,
        length=None,
        temperature=1,
        top_k=0,
        tune_name='',
        trunc_first=False
):
    """
    Interactively run the model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    :tune_name=None : String, subdir within the model_name dir where the fine tuned model lives,
     defaults to None, i.e. the base model
    :trunc_first=False : Boolean truncate each sample at the first end token
    """
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)

        temp = _get_temp(temperature)
        output = sample.sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=temp,
            top_k=top_k
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name, tune_name))
        saver.restore(sess, ckpt)

        while True:
            raw_text = input("title >>> ")
            while not raw_text:
                print('can not be empty')
                raw_text = input("title >>> ")
            text_in = sf.title_fmt(raw_text)
            tokens_in = enc.encode(text_in)
            gen(
                hparams,
                length,
                context,
                batch_size,
                temperature,
                top_k,
                nsamples,
                sess,
                enc,
                tokens_in,
                raw_text,
                trunc_first
            )


def _get_temp(temperature):
    try:
        return float(temperature)
    except ValueError:
        gauss = re.search(r'(?P<mu>\d*\.?\d*):(?P<sig>\d*\.?\d*)', str(temperature))
        mu, sig = gauss.group('mu'), gauss.group('sig') if gauss else (None, None)
        if mu and sig:
            return random.gauss(mu, sig)
        else:
            return 1


def gen(hparams, length, context, batch_size, temperature, top_k, nsamples, sess, enc, tokens_in, raw_in, trunc):
    n_toks = len(tokens_in)
    generated = 0
    for _ in range(nsamples // batch_size):
        temp = _get_temp(temperature)
        output = sample.sample_sequence(
            hparams=hparams,
            length=length,
            context=context,
            batch_size=batch_size,
            temperature=temp,
            top_k=top_k
        )
        batches = range(batch_size)
        out = sess.run(output, feed_dict={context: [tokens_in for _ in batches]})[:, n_toks:]
        for i in batches:
            generated += 1
            text = enc.decode(out[i])
            sf.print_output(text, raw_in, f'{generated} [t:{temp}]', trunc)


if __name__ == '__main__':
    fire.Fire(interact_model)
