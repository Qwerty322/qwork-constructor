import {IUserProfile} from '@/interfaces';

export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface Stock {
    ticker: string;
    country: string;
    url?: string;
    desc?: string;
    side?: number;
    price?: number;
    id: number;
}

export interface mainStock {
    symbol: string;
    country: string;
    name: string;
    currency?: string;
    change?: string;
    change_percentage?: string;
    last?: number;
    high?: number;
    low?: number;
    turnover?: number;
}

export interface Portfolio {
    stock_id?: number;
    owner_id?: number;
    stock: Stock;
    qty?: number;
    current_price?: number;
    id: number;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    userProfile: IUserProfile | null;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    stocks: Stock[];
    mainStocks: mainStock[];
    portfolio: Portfolio[];
    notifications: AppNotification[];
}


