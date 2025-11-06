
class Chapa():
    def __init__(self):
        pass
    def makePayment(self ,user , obj):
        import requests as req , os
        import uuid
        from dotenv import load_dotenv
       
       
        load_dotenv()
        
        api_key = os.getenv("SECRET_KEY")
        
        
        url = "https://api.chapa.co/v1/transaction/initialize"
        
        
        tx_ref =  f"chewatatest-{uuid.uuid4()}"
        
        
        payload = {
        "amount": str(obj.property_id.pricepernight),
        "currency": "ETB",
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        
        "tx_ref": tx_ref,
       
        "customization": {
            "title": "Listing",
            "description": "self.obj.description"
        }
         }

        headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
        }

        response = req.post(url, json=payload, headers=headers)
        data = response.json()  # Parse JSON directly
        data["tx_ref"] = tx_ref
       
        
        
        return data
    
    def verifypayment( self ,tx_ref):
        import requests , os
        
        from dotenv import load_dotenv
       
        load_dotenv()
        
        api_key = os.getenv("SECRET_KEY")
    
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        payload = ''
        headers = {
            'Authorization': f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers, data=payload)
        data = response.json()
        
        
        return data
 
        