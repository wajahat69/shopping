from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np
import pandas as pd
from database import supabase  


app = FastAPI()

templates = Jinja2Templates(directory='templates')

# Load model and scaler once
model = joblib.load("shopping_model.pkl")
scaler = joblib.load("shopping_scaler.pkl")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})

@app.post('/predict', response_class=HTMLResponse)
def prediction(request: Request,
               product_related: int = Form(...),
               product_related_duration: float = Form(...),
               page_values: float = Form(...),
               bounce_rates: float = Form(...),
               exit_rates: float = Form(...),
               special_day: float = Form(...),
               month: str = Form(...),
               weekend: str = Form(...),
               visitor_type: str = Form(...)
               ):

    # Encode categorical values
    month_mapping = {
        "Jan": 0, "Feb": 1, "Mar": 2,"Apr":3, "May": 4, "June": 5, "Jul": 6,
        "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    month_encoded = month_mapping.get(month[:3], 0)

    visitor_mapping = {
        "Returning Visitor": 1,
        "New Visitor": 0
    }
    visitor_encoded = visitor_mapping.get(visitor_type, 2)

    weekend_encoded = 1 if weekend.lower() == "yes" else 0

    # Input as DataFrame with proper column names
    input_dict = {
        "ProductRelated": [product_related],
        "ProductRelated_Duration": [product_related_duration],
        "BounceRates": [bounce_rates],
        "ExitRates": [exit_rates],
        "PageValues": [page_values],
        "SpecialDay": [special_day],
        "Month": [month_encoded],
        "VisitorType": [visitor_encoded],
        "Weekend": [weekend_encoded]
    }

    input_df = pd.DataFrame(input_dict)

    # Scale and predict
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]

    result = 'Will Purchase' if prediction == 1 else 'Will Not Purchase'

    # Save prediction to Supabase (uncomment to use)
    supabase.table("Shopping_predictions").insert({
            "ProductRelated": product_related,
            "ProductRelated_Duration": product_related_duration,
            "PageValues": page_values,
            "BounceRates": bounce_rates,
            "ExitRates": exit_rates,
            "SpecialDay": special_day,
            "Month": month,
            "Weekend": bool(weekend_encoded),
            "VisitorType": visitor_type,
            "Revenue": bool(prediction)
        }).execute()
    return templates.TemplateResponse('prediction.html', {
        'request': request,
        'result': result
    })
        



from mangum import Mangum
handler = Mangum(app)
