import axios from 'axios';
import {apiUrl} from '@/env';
import {IUserProfile, IUserProfileUpdate, IUserProfileCreate, IPortfolio} from './interfaces';

function authHeaders(token: string) {
    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
}

export const api = {
    async logInGetToken(username: string, password: string) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
    },
    async getMe(token: string) {
        return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
    },
    async updateMe(token: string, data: IUserProfileUpdate) {
        return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
    },
    async getUsers(token: string) {
        return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
    },
    async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
        return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
    },
    async createUser(token: string, data: IUserProfileCreate) {
        return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
    },
    async getStocks(token: string) {
        return axios.get(`${apiUrl}/api/v1/utils/stocks/`, authHeaders(token));
    },
    async getMainStocks(token: string) {
        return axios.get(`${apiUrl}/api/v1/utils/all-stocks/`, authHeaders(token));
    },
    async getPortfolio(token: string) {
        return axios.get(`${apiUrl}/api/v1/items/`, authHeaders(token));
    },
    async addToPortfolio(token: string, data: IPortfolio) {
        return axios.post(`${apiUrl}/api/v1/items/`, data, authHeaders(token));
    },
    async removeFromPortfolio(token: string, data: number) {
        return axios.delete(`${apiUrl}/api/v1/items/${data}`, authHeaders(token));
    },
    async passwordRecovery(email: string) {
        return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
    },
    async resetPassword(password: string, token: string) {
        return axios.post(`${apiUrl}/api/v1/reset-password/`, {
            new_password: password,
            token,
        });
    },
};
