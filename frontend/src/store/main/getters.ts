import {MainState} from './state';
import {getStoreAccessors} from 'typesafe-vuex';
import {State} from '../state';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    loginError: (state: MainState) => state.logInError,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    userProfile: (state: MainState) => state.userProfile,
    stocksInPortfolio: (state: MainState) => state.portfolio,
    stocksForBuy: (state: MainState) => state.stocks.filter((value) => value.side === 1),
    stocksForSell: (state: MainState) => state.stocks.filter((value) => value.side === 2),
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readStocksInPortfolio = read(getters.stocksInPortfolio);
export const readStocksForBuy = read(getters.stocksForBuy);
export const readStocksForSell = read(getters.stocksForSell);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
