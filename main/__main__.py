from app import create_app
import sys
sys.path.append(".")

app = create_app()

if __name__ == "__main__":
    app.run(host = '26.112.158.194', debug=True) #host = '26.112.158.194',
    
