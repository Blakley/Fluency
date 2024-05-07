# Seq2Seq-Translation
Implementation of a Sequence-to-Sequence (Seq2Seq) model for language translation using deep learning.

---

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

# Transforming <span style="color: #1a73e8;">English</span> to <span style="color: #e83e1a;">French</span> Language Translation

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Data Loading

<span id="data-loading-1"></span>

We will use a diverse dataset containing **English-French** bilingual
sentence pairs to train our deep learning model.Our dataset will include
a combination of sentences sourced from
<a href="https://www.manythings.org/anki/" target="_blank">Anki</a>'s
language database and additional pairs collected from authors on
<a href="https://www.memrise.com/en-us/" target="_blank">Memrise</a>, a
language-learning platform.The objective is to create a robust training
set that captures a wide range of language patterns and translations for
effective model training.

- 💾 Access the dataset containing *200 thousand* delimited bilingual
  sentence pairs.
- 💾 Integrate the additional dataset extracted from Memrise, consisting
  of *several thousand* English-French sentence pairs contributed by
  French-speaking authors.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### GPU Check<a href="#GPU-Check" class="anchor-link"></a>

- 🖥️ Model testing and training was conducted using a dedicated GPU,
  this check ensures that the GPU is selected.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">


<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">


<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### Loading The data<a href="#Loading-The-data" class="anchor-link"></a>

- Load the compiled English-French language pairs file

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">


<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

```python
    import pandas as pd

    # load the csv data (small version for testing, large for actual deployment)
    df = pd.read_csv('small.txt', names=['english_text', 'french_text', 'attr'], usecols=['english_text', 'french_text'], sep='\t')

    df = df.sample(frac=1, random_state=42)
    df = df.reset_index(drop=True)

    print(f"Dataset length: {len(df)}")
```

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Data Preparation

<span id="data-preparation-2"></span>

In this section, we will prepare our dataset for training by performing
the following tasks:

- Clean the text data by removing punctuation symbols, numbers, and
  converting characters to lowercase.
- Replace Unicode characters with their ASCII equivalents.
- Determine the maximum sequence length of both English and French
  phrases to establish input and output sequence lengths for our model.

🔑 These steps are crucial for ensuring that our data is properly
formatted and ready to be used for training our deep learning model.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### Handling language data formatting<a href="#Handling-language-data-formatting" class="anchor-link"></a>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">


</div>

<div class="jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output jp-OutputArea-executeResult"
mime-type="text/html">

<div>

<table class="dataframe" data-border="1">
<thead>
<tr class="header" style="text-align: right;">
<th></th>
<th>english_text</th>
<th>french_text</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<th>0</th>
<td>youre very clever</td>
<td>[start] vous etes fort ingenieuse [end]</td>
</tr>
<tr class="even">
<th>1</th>
<td>are there kids</td>
<td>[start] y atil des enfants [end]</td>
</tr>
<tr class="odd">
<th>2</th>
<td>come in</td>
<td>[start] entrez [end]</td>
</tr>
<tr class="even">
<th>3</th>
<td>wheres boston</td>
<td>[start] ou est boston [end]</td>
</tr>
<tr class="odd">
<th>4</th>
<td>you see what i mean</td>
<td>[start] vous voyez ce que je veux dire [end]</td>
</tr>
</tbody>
</table>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>


</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Language Tokenization

<span id="language-tokenization-3"></span>

⚒️ We will tokenize the English and French phrases using separate
Tokenizer instances and generate padded sequences for model training.
The steps involved are as follows:

1.  Fit a Tokenizer to the English phrases and another Tokenizer to
    their French equivalents.
2.  Compute the vocabulary sizes based on the Tokenizer instances.
3.  Create padded sequences for all phrases.
4.  Prepare features and labels for training:

- The features consist of the padded English sequences and the padded
  French sequences excluding the `[end]` tokens.
- The labels consist of the padded French sequences excluding the
  `[start]` tokens.

🔑 These steps will put the features into a dictionary format suitable
for inputting into our mode

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

### Fit the language tokenizers<a href="#Fit-the-language-tokenizers" class="anchor-link"></a>

⚙️ Tokenizers are fitted to the training data to convert our text into a
format that the neural network can process numerically.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

```python
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    # Tokenizing English text using Tokenizer
    english_tokenizer  = Tokenizer() 
    english_tokenizer .fit_on_texts(english_text)
    english_sequences = english_tokenizer .texts_to_sequences(english_text)
    english_x = pad_sequences(english_sequences, maxlen=sequence_len, padding='post')

    # Tokenizing French text using Tokenizer  
    special = '!"#$%&()*+,-./:;<=>?@\\^_`{|}~\t\n'
    french_tokenizer  = Tokenizer(filters = special)
    french_tokenizer .fit_on_texts(french_text)
    french_sequences = french_tokenizer .texts_to_sequences(french_text)
    french_y = pad_sequences(french_sequences, maxlen=sequence_len + 1, padding='post')
```

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">


<table>
<tbody>
<tr class="odd">
<td><u>Model Input Dimensions</u></td>
<td style="text-align: left;">Vocabulary size determines the range of
possible input tokens.</td>
</tr>
<tr class="even">
<td><u>Embedding Matrix</u></td>
<td style="text-align: left;">Each word in the vocabulary corresponds to
an embedding vector learned by the model during training.</td>
</tr>
<tr class="odd">
<td><u>Output Layer Dimensions</u></td>
<td style="text-align: left;">Vocabulary size of the target language
determines the dimensionality of the model's output layer.</td>
</tr>
</tbody>
</table>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

```python
    english_vocabulary_size = len(english_tokenizer.word_index) + 1
    french_vocabulary_size = len(french_tokenizer.word_index) + 1

    print(f'Vocabulary size (English) : {english_vocabulary_size}') # 6033
    print(f'Vocabulary size (French)  : {french_vocabulary_size}')  # 12197
```

</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>


</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Model Architecture

<span id="model-architecture-4"></span>

Below is an outline of the model architecture:

1.  Define a stack of transformer layers.
2.  Define the transformer decoder that accepts the output of the
    transformer layers along with the padded French sequences.
3.  Connect the transformer layers and decoder components to create the
    full transformer model.
4.  Add a softmax output layer to the decoder for classification.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Model Training and Evaluation

<span id="model-training-evaluation-5"></span>

We train 🚂 the model and evaluate its performance on the validation
set. The training process will include the following steps:

1.  Train the model using the training data.
2.  Use `EarlyStopping` callback to monitor validation accuracy and stop
    training if it fails to improve for 5 epochs.
3.  Plot the training and validation accuracy to visualize the model's
    learning progress.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### Evaluate the model's performance

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedText jp-OutputArea-output"
mime-type="text/plain">

    1563/1563 [==============================] - 14s 9ms/step - loss: 0.2290 - accuracy: 0.8512
    Test Loss: 0.22895030677318573
    Validation Accuracy: 0.8511516451835632

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### Assess the model's learning accuracy

![Image Alt Text](src/training.PNG)

<div class=" cm-s-jupyter">



</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output"
mime-type="text/html">

</div>

</div>

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedHTML jp-OutputArea-output"
mime-type="text/html">

<div>

<div id="b3bdc257-1558-4a9f-9958-dfe568568927" class="plotly-graph-div"
style="height:525px; width:100%;">

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Translation Testing

<span id="translation-testing-6"></span>

Handle the translation process based on the model's predictions.

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">



</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedText jp-OutputArea-output"
mime-type="text/plain">

    English: let us out of here => French: laissenous sortir dici
    English: it could be fun => French: ca pourrait etre marrant
    English: this is my new video => French: cest ma nouvelle video
    English: do you like fish => French: aimestu le poisson
    English: you were in a coma => French: vous etiez dans le coma
    English: dont be upset => French: ne soyez pas fache
    English: didnt you know that => French: le saviezvous
    English: im not exactly sure => French: je nen suis pas a la tete
    English: i put it on your desk => French: je lai mise sur votre bureau
    English: somehow tom knew => French: pourtant tom savait

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

## Translation Comparison

<span id="translation-comparison-7"></span>

Compare against Baseline model is:
<a href="https://github.com/LibreTranslate/LibreTranslate"
target="_blank">LibreTranslate</a> which uses a NMT Model architecture

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">



</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">


</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>


</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedText jp-OutputArea-output"
mime-type="text/plain">

    English: let us out of here => French: laissez-nous sortir d'ici
    English: it could be fun => French: ça pourrait être amusant
    English: this is my new video => French: c'est ma nouvelle vidéo
    English: do you like fish => French: vous aimez le poisson
    English: you were in a coma => French: tu étais dans le coma
    English: dont be upset => French: ne soyez pas contrarié
    English: didnt you know that => French: tu ne savais pas que
    English: im not exactly sure => French: im pas exactement sûr
    English: i put it on your desk => French: je l'ai mis sur ton bureau
    English: somehow tom knew => French: tom le savait

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
mime-type="text/markdown">

#### Compare the Baseline model (NMT) to our Model (Seq2Seq)

- Use NLTK's edit_distance to calculate the similarity score between the
  translations produced by each model
- Calculate the average similarity score across all pairs of
  translations

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">


</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">



</div>

</div>

</div>

</div>

<div class="jp-Cell-outputWrapper">

<div class="jp-Collapser jp-OutputCollapser jp-Cell-outputCollapser">

</div>

<div class="jp-OutputArea jp-Cell-outputArea">

<div class="jp-OutputArea-child">

<div class="jp-OutputPrompt jp-OutputArea-prompt">

</div>

<div class="jp-RenderedText jp-OutputArea-output"
mime-type="text/plain">

    seq2seq model ==> English: let us out of here => French: laissenous sortir dici
    nmt model     ==> English: let us out of here => French: laissez-nous sortir d'ici
    Similarity score: 0.9091

    seq2seq model ==> English: it could be fun => French: ca pourrait etre marrant
    nmt model     ==> English: it could be fun => French: ça pourrait être amusant
    Similarity score: 0.8125

    seq2seq model ==> English: this is my new video => French: cest ma nouvelle video
    nmt model     ==> English: this is my new video => French: c'est ma nouvelle vidéo
    Similarity score: 0.9355

    seq2seq model ==> English: do you like fish => French: aimestu le poisson
    nmt model     ==> English: do you like fish => French: vous aimez le poisson
    Similarity score: 0.7241

    seq2seq model ==> English: you were in a coma => French: vous etiez dans le coma
    nmt model     ==> English: you were in a coma => French: tu étais dans le coma
    Similarity score: 0.7742

    seq2seq model ==> English: dont be upset => French: ne soyez pas fache
    nmt model     ==> English: dont be upset => French: ne soyez pas contrarié
    Similarity score: 0.7333

    seq2seq model ==> English: didnt you know that => French: le saviezvous
    nmt model     ==> English: didnt you know that => French: tu ne savais pas que
    Similarity score: 0.5357

    seq2seq model ==> English: im not exactly sure => French: je nen suis pas a la tete
    nmt model     ==> English: im not exactly sure => French: im pas exactement sûr
    Similarity score: 0.3636

    seq2seq model ==> English: i put it on your desk => French: je lai mise sur votre bureau
    nmt model     ==> English: i put it on your desk => French: je l'ai mis sur ton bureau
    Similarity score: 0.8333

    seq2seq model ==> English: somehow tom knew => French: pourtant tom savait
    nmt model     ==> English: somehow tom knew => French: tom le savait
    Similarity score: 0.6296

    Average similarity score: 0.7251

</div>

</div>

</div>

</div>

</div>

<div class="jp-Cell jp-CodeCell jp-Notebook-cell jp-mod-noOutputs">

<div class="jp-Cell-inputWrapper">

<div class="jp-Collapser jp-InputCollapser jp-Cell-inputCollapser">

</div>

<div class="jp-InputArea jp-Cell-inputArea">

<div class="jp-InputPrompt jp-InputArea-prompt">

</div>

<div class="jp- jp-Editor jp-InputArea-editor"
data-type="inline">

<div class=" cm-s-jupyter">

<div class="highlight hl-ipython3">

     

</div>

</div>

</div>

</div>

</div>

</div>
