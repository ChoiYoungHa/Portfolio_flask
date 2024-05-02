from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

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
        return jsonify({"error": "자막을 찾을 수 없습니다. 비디오가 자막을 지원하지 않거나 요청된 언어가 지원되지 않을 수 있습니다."}), 404
    except VideoUnavailable:
        return jsonify({"error": "비디오 ID가 유효하지 않거나 비디오가 사용할 수 없습니다. 비디오 ID를 확인하세요."}), 404
    except ConnectionError:
        return jsonify({"error": "YouTube에 연결할 수 없습니다. 네트워크 연결을 확인하고 다시 시도하세요."}), 503
    except Exception as e:
        return jsonify({"error": "알 수 없는 오류가 발생했습니다: " + str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
