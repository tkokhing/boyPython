import pandas as pd

def sample_200_domains():
    df = pd.read_csv("top-1m.csv")
    return df.sample(n=200)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = sample_200_domains()
    df.columns = ["S/N", "Domain"]
    df.to_csv("200.csv", index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
