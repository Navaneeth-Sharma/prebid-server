from flask import Flask, request, jsonify
import gzip
import json


app = Flask(__name__)

@app.route('/bidder-endpoint', methods=['POST'])
def bidder_endpoint():
    try:
        data = gzip.decompress(request.data).decode("utf-8")

        # Get JSON data from request
        json_data = json.loads(data)

        # Extract necessary fields
        request_id = json_data.get("id", "")
        imps = json_data.get("imp", [])

        seatbid = []
        bids = []

        for imp in imps:
            impid = imp.get("id", "")
            if impid:
                bid = {
                    "id": f"bid-{impid}",
                    "impid": impid,
                    "price": round(1.0 + 0.1 * len(impid), 2),  # Dummy price logic
                    "crid": f"creative-{impid}",
                    "adm": f"<html>Test Ad {impid}</html>"
                }
                bids.append(bid)

        if bids:
            seatbid.append({"bid": bids})

        response = {
            "id": request_id,
            "seatbid": seatbid,
            "cur": "USD"
        }

        return json.dumps(response, indent=2)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8081)
