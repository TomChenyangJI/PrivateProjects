import whisper
import warnings
from transformers import pipeline
import ssl


warnings.filterwarnings('ignore')
ssl._create_default_https_context = ssl._create_unverified_context


def get_transcription(vid_path):
    print("Generating transcription...")
    model = whisper.load_model("base")
    result = model.transcribe(vid_path)
    transcription = result["text"]
    return transcription


def get_summary(transcription):
    # Load summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split the transcription if it's too long for the model to handle at once
    max_chunk_size = 1024
    chunks = [transcription[i:i + max_chunk_size] for i in range(0, len(transcription), max_chunk_size)]

    print("I am creating the summary now, please be patient, the result is coming soon ...")

    # Summarize each chunk and combine the summaries
    summary = " ".join(
        [summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks])

    return summary


def get_summary_chinese(transcription):
    from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

    print("Generating the summary ...")
    # Load the tokenizer and model
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    # Tokenize the transcription
    inputs = tokenizer(transcription, return_tensors="pt", max_length=1024, truncation=True)

    # Generate the summary
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # print("Summary:\n", summary)
    return summary


vid_path = 'yt_test/鋼琴廣告.mp4'
print(get_summary_chinese(get_transcription(vid_path)))

"""
generate the transcription for each video first, then concatenate the transcriptions, 
input the concatenated transcription to the summary function
"""
