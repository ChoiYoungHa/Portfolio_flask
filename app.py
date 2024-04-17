from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/getSubtitle')
def get_subtitle():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({"error": "동영상이 존재하지 않습니다."}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        refined_transcript = [entry['text'] for entry in transcript]
        return jsonify(refined_transcript)
    except NoTranscriptFound:
        return jsonify({"error": "해당 동영상은 자막을 지원하지 않거나 한국영상이 아닙니다."}), 404
    except TranscriptsDisabled:
        return jsonify({"error": "해당 동영상에서는 자막 사용이 비활성화되어 있습니다."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
