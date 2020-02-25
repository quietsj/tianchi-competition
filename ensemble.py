kf = StratifiedKFold(shuffle=True, random_state=np.random.randint(0, 10000))
fun = lambda x, y: x + y
from functools import reduce

train_val = []
train_test = []
for clf in [gbdt, xgb, lgb]:
    st_val = []
    st_test = []
    val_label = []
    for train_index, val_index in kf.split(train, label):
        x_train, y_train = train.iloc[train_index], label.iloc[train_index]
        x_val, y_val = train.iloc[val_index], label.iloc[val_index]
        x_train_new, x_val_new, x__test_new = pre_processing(x_train, y_train, [x_train, x_val, test], [var, sel])
        clf.fit(x_train_new, y_train)

        pre_val = clf.predict_proba(x_val_new)
        pre_test = clf.predict_proba(x__test_new)
        st_val.append(pd.DataFrame(pre_val))
        st_test.append(pd.DataFrame(pre_test))
        val_label.append(y_val)
    st_val = pd.concat(st_val, axis=0)
    val_label = pd.concat(val_label, axis=0)
    st_test = reduce(fun, st_test) / len(st_test)
    train_val.append(st_val)
    train_test.append(st_test)
train_val = pd.concat(train_val, axis=1)
train_test = pd.concat(train_test, axis=1)
svm = SVC(kernel='linear')
svm.fit(train_val, val_label)
pre_result = svm.predict(train_test)
res = pd.concat([test_id, pd.DataFrame(pre_result)], axis=1)
res.to_csv('./resultB_2.csv', sep=',', header=False, index=False, encoding='utf-8')