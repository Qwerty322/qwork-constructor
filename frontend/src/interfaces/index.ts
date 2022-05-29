export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    need_notification: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    need_notification?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    need_notification?: boolean;
}

export interface IStock {
    ticker: string;
    country: string;
    url?: string;
    desc?: string;
    side?: number;
    price?: number;
    id: number;
}

export interface IPortfolio {
    qty?: number;
    stock_id?: number;
}
