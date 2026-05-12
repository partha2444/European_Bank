"""
ML Engine for Churn Prediction and Risk Scoring.
Trains a Random Forest model on bank customer data and provides
churn probabilities, risk tiers, feature importances, and evaluation metrics.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)


def prepare_features(df):
    """Encode categoricals and select features for modeling."""
    feature_df = df.copy()
    le_geo = LabelEncoder()
    le_gen = LabelEncoder()
    feature_df['Geography_enc'] = le_geo.fit_transform(feature_df['Geography'])
    feature_df['Gender_enc'] = le_gen.fit_transform(feature_df['Gender'])

    feature_cols = [
        'CreditScore', 'Geography_enc', 'Gender_enc', 'Age', 'Tenure',
        'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
    ]
    X = feature_df[feature_cols]
    y = feature_df['Exited']
    return X, y, feature_cols


def train_model(df, model_type='random_forest', test_size=0.2, random_state=42):
    """Train a classifier and return model, metrics, and predictions."""
    X, y, feature_cols = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    if model_type == 'gradient_boosting':
        model = GradientBoostingClassifier(
            n_estimators=200, max_depth=5, learning_rate=0.1, random_state=random_state
        )
    else:
        model = RandomForestClassifier(
            n_estimators=200, max_depth=10, min_samples_split=5,
            random_state=random_state, n_jobs=-1
        )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba),
    }

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred)

    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return {
        'model': model,
        'metrics': metrics,
        'fpr': fpr, 'tpr': tpr,
        'confusion_matrix': cm,
        'feature_importances': importances,
        'feature_cols': feature_cols,
        'X_test': X_test, 'y_test': y_test,
        'y_pred': y_pred, 'y_proba': y_proba
    }


def predict_risk_scores(df, model, feature_cols):
    """Generate churn probability and risk tier for every customer."""
    X, _, _ = prepare_features(df)
    X = X[feature_cols]
    proba = model.predict_proba(X)[:, 1]
    result = df.copy()
    result['ChurnProbability'] = (proba * 100).round(1)
    result['RiskTier'] = pd.cut(
        result['ChurnProbability'],
        bins=[-1, 20, 40, 70, 101],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    return result
