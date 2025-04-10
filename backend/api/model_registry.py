from data_analytics.pk_naive import PKNaiveBayes
from data_analytics.pk_quantile import PKQuantileRegressor
from data_analytics.yl_naive import YLNaiveBayes
from data_analytics.yl_quantile import YLQuantileRegressor
from data_analytics.srt_naive import SRTNaiveBayes
from data_analytics.srt_quantile import SRTQuantileRegressor
from data_analytics.rl_naive import RLNaiveBayes
from data_analytics.rl_quantile import RLQuantileRegressor
from data_analytics.arl_naive import ARLNaiveBayes
from data_analytics.arl_quantile import ARLQuantileRegressor
from data_analytics.mrt_naive import MRTNaiveBayes
from data_analytics.mrt_quantile import MRTQuantileRegressor
from data_analytics.bts_naive import BTSNaiveBayes
from data_analytics.bts_quantile import BTSQuantileRegressor
from data_analytics.constant import RATING_MAP

pk_nb = None
pk_qr = None
yl_nb = None
yl_qr = None
srt_nb = None
srt_qr = None
rl_nb = None
rl_qr = None
arl_nb = None
arl_qr = None
mrt_nb = None
mrt_qr = None
bts_nb = None
bts_qr = None
rating_map = RATING_MAP

def init_models():
    global pk_nb, pk_qr, yl_nb, yl_qr, srt_nb, srt_qr, rl_nb, rl_qr, arl_nb, arl_qr, mrt_nb, mrt_qr, bts_nb, bts_qr

    p_nb = PKNaiveBayes()
    p_df = p_nb.preprocess()
    p_nb.train(p_df)
    p_nb.evaluate()
    p_qr = PKQuantileRegressor()
    X_train, X_test, y_train, y_test = p_qr.preprocess(p_df, rating_map)
    p_qr.train(X_train, y_train, X_test, y_test)
    p_qr.evaluate()
    pk_nb = p_nb
    pk_qr = p_qr

    y_nb = YLNaiveBayes()
    y_df = y_nb.preprocess()
    y_nb.train(y_df)
    y_nb.evaluate()
    y_qr = YLQuantileRegressor()
    X_train, X_test, y_train, y_test = y_qr.preprocess(y_df, rating_map)
    y_qr.train(X_train, y_train, X_test, y_test)
    y_qr.evaluate()
    yl_nb = y_nb
    yl_qr = y_qr

    s_nb = SRTNaiveBayes()
    s_df = s_nb.preprocess()
    s_nb.train(s_df)
    s_nb.evaluate()
    s_qr = SRTQuantileRegressor()
    X_train, X_test, y_train, y_test = s_qr.preprocess(s_df, rating_map)
    s_qr.train(X_train, y_train, X_test, y_test)
    s_qr.evaluate()
    srt_nb = s_nb
    srt_qr = s_qr

    r_nb = RLNaiveBayes()
    r_df = r_nb.preprocess()
    r_nb.train(r_df)
    r_nb.evaluate()
    r_qr = RLQuantileRegressor()
    X_train, X_test, y_train, y_test = r_qr.preprocess(r_df, rating_map)
    r_qr.train(X_train, y_train, X_test, y_test)
    r_qr.evaluate()
    rl_nb = r_nb
    rl_qr = r_qr

    a_nb = ARLNaiveBayes()
    a_df = a_nb.preprocess()
    a_nb.train(a_df)
    a_nb.evaluate()
    a_qr = ARLQuantileRegressor()
    X_train, X_test, y_train, y_test = a_qr.preprocess(a_df, rating_map)
    a_qr.train(X_train, y_train, X_test, y_test)
    a_qr.evaluate()
    arl_nb = a_nb
    arl_qr = a_qr

    m_nb = MRTNaiveBayes()
    m_df = m_nb.preprocess()
    m_nb.train(m_df)
    m_nb.evaluate()
    m_qr = MRTQuantileRegressor()
    X_train, X_test, y_train, y_test = m_qr.preprocess(m_df, rating_map)
    m_qr.train(X_train, y_train, X_test, y_test)
    m_qr.evaluate()
    mrt_nb = m_nb
    mrt_qr = m_qr

    b_nb = BTSNaiveBayes()
    b_df = b_nb.preprocess()
    b_nb.train(b_df)
    b_nb.evaluate()
    b_qr = BTSQuantileRegressor()
    X_train, X_test, y_train, y_test = b_qr.preprocess(b_df, rating_map)
    b_qr.train(X_train, y_train, X_test, y_test)
    b_qr.evaluate()
    bts_nb = b_nb
    bts_qr = b_qr
