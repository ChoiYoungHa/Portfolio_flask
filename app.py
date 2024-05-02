import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

app = Flask(__name__)

# 로깅설정
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

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
    except NoTranscriptFound as e:
        app.logger.exception("No transcript found for video ID: {}".format(video_id))
        return jsonify({"error": "자막을 찾을 수 없습니다. 비디오가 자막을 지원하지 않거나 요청된 언어가 지원되지 않을 수 있습니다."}), 403
    except TranscriptsDisabled:
        return jsonify({"error": "이 동영상에서는 자막 기능이 비활성화되어 있습니다. 동영상 소유자가 자막 사용을 허용하지 않았을 수 있습니다."}), 403
    except VideoUnavailable as e:
        app.logger.exception("Video unavailable: {}".format(video_id))
        return jsonify({"error": "비디오 ID가 유효하지 않거나 비디오가 사용할 수 없습니다. 비디오 ID를 확인하세요."}), 404
    except ConnectionError as e:
        app.logger.exception("Failed to connect to YouTube")
        return jsonify({"error": "YouTube에 연결할 수 없습니다. 네트워크 연결을 확인하고 다시 시도하세요."}), 503
    except Exception as e:
        message = str(e)
        app.logger.exception("Unknown error occurred : " + message)
        return jsonify({"error": "알 수 없는 오류가 발생했습니다: " + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
