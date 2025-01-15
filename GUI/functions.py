import joblib, os

def predict_weather_id(dates:list[str]):

    for model_features in os.walk(r"D:\STUCOM\Master_IABD\Projecte3_Meteorologia\Entregables\Code\Prophet\models"):
        model_features.predict()


    model_weather_id = joblib.load(r"D:\STUCOM\Master_IABD\Projecte3_Meteorologia\Entregables\Code\SVM\weather_id_svm_model_v1.pkl")