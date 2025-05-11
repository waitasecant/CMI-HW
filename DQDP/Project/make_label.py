# Make labels based on cleanset exported from Cleanlab Studio
import pandas as pd

df = pd.read_csv('cleanlab-faces-expr.csv')

# 1. Replace values in 'cleanlab_suggested_label_original' and 'cleanlab_suggested_label_pred' 
# where 'cleanlab_action' is not 'unresolved'
mask = df['cleanlab_action'] != 'unresolved'
df.loc[mask, 'cleanlab_suggested_label_original'] = df.loc[mask, 'expression']
df.loc[mask, 'cleanlab_suggested_label_pred'] = df.loc[mask, 'expression']

# 2. Replace values based on the specified conditions
not_out_amb = ~((df['cleanlab_is_outlier'] == False) & (df['cleanlab_is_ambiguous'] == False))
no_label_issue = df['cleanlab_is_label_issue'] == False
mask = not_out_amb & no_label_issue

df.loc[mask, 'cleanlab_suggested_label_original'] = df.loc[mask, 'expression']
df.loc[mask, 'cleanlab_suggested_label_pred'] = df.loc[mask, 'cleanlab_predicted_label']

# 3. Replace the file extension from .png to .pgm in the image column
df['image'] = df['image'].str.replace('.png', '.pgm')

# Save the modified dataframe back to CSV
df.to_csv('modified-cleanlab-faces-expr.csv', index=False)