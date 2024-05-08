# Fluency - Language Learning Desktop Application

- A desktop notification app that uses a Seq2Seq model to allow users to create various language notifications.
---

![Image Alt Text](src/create.PNG)

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


## Data Preparation

<span id="data-preparation-2"></span>

In this section, we will prepare our dataset for training by performing
the following tasks:

- Clean the text data by removing punctuation symbols, numbers, and
  converting characters to lowercase.
- Replace Unicode characters with their ASCII equivalents.
- Determine the maximum sequence length of both English and French
  phrases to establish input and output sequence lengths for our model.


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
set. Below are the current learning assessment metrics.

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
