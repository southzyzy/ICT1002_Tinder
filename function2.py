class COUNTRY_MATCH:
    def __init__(self, df, name):
        student_B = df.loc[df["Name"] == name].apply(lambda x : (x["Name"], x["Gender"], x['Acceptable_country']), axis=1)
        student_B_gender = student_B.values[0][1]
        student_B_country = student_B.values[0][2].split(", ")
        self.matched = df.loc[df['Country'].isin(student_B_country) & (df['Name'] != name) & (df['Gender'] != student_B_gender)].apply(lambda x : (x["Name"], x['Gender'], x['Country']), axis=1)



