from flask import Blueprint
from flask_restful import Api, Resource
import pandas as pd

price_api = Blueprint('price_api', __name__)
api = Api(price_api)

class PriceAPI(Resource):
    def get(self):
        try:
            # Read the CSV file
            df = pd.read_csv('volume/data.csv')
            
            # Calculate discount percentage
            df['discount'] = ((df['average_price'] - df['current_price']) / df['average_price']) * 100
            
            # Sort by discount
            sorted_discounts = df.sort_values(by='discount', ascending=False)
            
            # Create list of dictionaries with all product information
            result = []
            seen_asins = set()
            for _, row in sorted_discounts.iterrows():
                if row['asin'] not in seen_asins:
                    result.append({
                        'name': row['name'],
                        'image': f"{row['asin']}.jpg",  # Construct image path using ASIN
                        'current_price': float(row['current_price']),
                        'original_price': float(row['average_price']),
                        'discount': round(float(row['discount']), 2),  # Round to 2 decimal places
                        'link': f"https://www.amazon.com/dp/{row['asin']}"
                    })
                    seen_asins.add(row['asin'])
                if len(result) == 5:
                    break
            
            return {
                "topdiscount": result
            }
        except FileNotFoundError:
            return {"error": "Data file not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(PriceAPI, '/api/price')