import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, confusion_matrix, classification_report
)
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression


# returnera alla viktiga typer av eda, typ df.info(), df.shape, df.describe(), df.value.counts(), df.columns, vilka korrelationer kolumnerna har, pairplot, heatmap, boxplot och ta bort outliers
def eda(df, drop_outliers=False, outlier_factor=1.5):
    """
    Gör en enkel EDA på en DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame som ska analyseras
    drop_outliers : bool
        Om True → ta bort outliers baserat på IQR
    outlier_factor : float
        Multipel av IQR som bestämmer cutoff (default=1.5)
        
    Example use:
        clean_df = eda(my_dataframe, drop_outliers=True)
    """

    print("=== Shape ===")
    print(df.shape)

    print("\n=== Columns ===")
    print(df.columns.tolist())

    print("\n=== Info ===")
    print(df.info())

    print("\n=== Describe ===")
    print(df.describe(include="all"))

    print("\n=== Value counts (för kategoriska variabler) ===")
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    for col in cat_cols:
        print(f"\n{col}:\n", df[col].value_counts())

    # Korrelationer
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        corr = num_df.corr()
        print("\n=== Correlation matrix ===")
        print(corr)

        # Heatmap
        plt.figure(figsize=(10,6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.show()

        # Pairplot (kan bli tungt för många variabler)
        if num_df.shape[1] <= 6:  # begränsa så det inte blir för plot-heavy
            sns.pairplot(num_df)
            plt.show()

        # Boxplots för varje numerisk variabel
        for col in num_df.columns:
            plt.figure(figsize=(6,4))
            sns.boxplot(x=df[col])
            plt.title(f"Boxplot of {col}")
            plt.show()

        # Ta bort outliers (IQR-metoden)
        if drop_outliers:
            clean_df = df.copy()
            for col in num_df.columns:
                Q1 = clean_df[col].quantile(0.25)
                Q3 = clean_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - outlier_factor * IQR
                upper = Q3 + outlier_factor * IQR
                clean_df = clean_df[(clean_df[col] >= lower) & (clean_df[col] <= upper)]
            print(f"\nEfter outlier removal: {clean_df.shape}")
            return clean_df

    return df


# lägg till generell funktion som tar emot en eller flera modeller(knn, random forest, linear/logistic regression) och gör alla stegen
def predict(models, features, target, test_size=0.2, val_size=0.2, random_state=42, scaler="standard"):
    """
    Generell funktion för att träna/testa en eller flera sklearn-modeller.
        Parameters
        ----------
        models : dict
            { "ModelName": sklearn_model }
        features : pd.DataFrame
            Input features
        target : pd.Series
            Target values
        scaler : str
            "standard" -> StandardScaler
            "minmax"   -> MinMaxScaler
            None       -> Ingen scaling
    
    Returnerar en dataframe med jämförelser.
    
    Exempel: 
    classification:
    models = {
        "KNN": KNeighborsClassifier(),
        "RandomForest": RandomForestClassifier(),
        "LogReg": LogisticRegression(max_iter=1000)
    }
    regression:
    models = {
        "KNN": KNeighborsRegressor(),
        "RandomForest": RandomForestRegressor(),
        "LinearReg": LinearRegression()
    }

    df_results = predict(models, X, y)
    """
    
    X = features.copy()
    y = target.copy()

    # Train/Val/Test split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size+val_size, random_state=random_state)
    rel_test_size = test_size / (test_size + val_size)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=rel_test_size, random_state=random_state)

    results = []

    for name, model in models.items():
        print(f"\n=== Tränar {name} ===")

        # Bestäm typ av uppgift (klassificering vs regression)
        is_classification = "Classifier" in model.__class__.__name__

        # Scaling / Encoding
        numeric_features = X.select_dtypes(include=[np.number]).columns
        categorical_features = X.select_dtypes(exclude=[np.number]).columns

        transformers = []
        if len(numeric_features) > 0:
            # Scaling behövs för KNN och linjär regression, inte alltid för träd
            if isinstance(model, (KNeighborsClassifier, KNeighborsRegressor, LogisticRegression, LinearRegression)):
                transformers.append(("num", StandardScaler(), numeric_features))
        if len(categorical_features) > 0:
            transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features))

        preprocessor = ColumnTransformer(transformers, remainder="passthrough")
        pipe = Pipeline([("preprocessor", preprocessor), ("model", model)])

        # Hyperparam tuning exempel för KNN
        if isinstance(model, (KNeighborsClassifier, KNeighborsRegressor)):
            param_grid = {"model__n_neighbors": range(1, 11)}
            search = GridSearchCV(pipe, param_grid, cv=3, scoring="accuracy" if is_classification else "neg_mean_squared_error")
            search.fit(X_train, y_train)
            best_model = search.best_estimator_
        else:
            best_model = pipe.fit(X_train, y_train)

        # Utvärdera
        y_pred = best_model.predict(X_test)

        if is_classification:
            report = classification_report(y_test, y_pred, output_dict=True)
            cm = confusion_matrix(y_test, y_pred)
            results.append({
                "Model": name,
                "Accuracy": report["accuracy"],
                "Precision (macro)": report["macro avg"]["precision"],
                "Recall (macro)": report["macro avg"]["recall"],
                "F1 (macro)": report["macro avg"]["f1-score"],
                "ConfusionMatrix": cm
            })
        else:
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            results.append({
                "Model": name,
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse
            })

    return pd.DataFrame(results)