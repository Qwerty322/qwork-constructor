<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">Welcome {{ greetedUser }}</div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/view">View Profile</v-btn>
        <v-btn to="/main/profile/edit">Edit Profile</v-btn>
        <v-btn to="/main/profile/password">Change Password</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Portfolio</div>
        <v-spacer></v-spacer>
        <b>Total: {{ totalPricePortfolio.toFixed(2) }}₽</b>
      </v-card-title>
      <v-card-text>
        <v-container
            fluid
            grid-list-lg
        >
          <v-layout row wrap>
            <v-flex xs12 v-for="item in stockPortfolio">
              <v-card>
                <v-card-title primary-title>
                  <div class="headline">Ticker:
                    <a target="_blank"
                       rel="noopener noreferrer"
                       :href="item.stock.url">
                      {{ item.stock.ticker }}
                    </a>
                  </div>
                  <v-spacer></v-spacer>
                  <b>Total: {{ (item.current_price * item.qty).toFixed(2) }}₽</b>
                  <span
                      :class="item.stock.price <= item.current_price ? 'green--text': 'red--text'"> ({{
                      ((item.current_price - item.stock.price) * item.qty).toFixed(2)
                    }}₽)</span>
                </v-card-title>
                <v-card-text>
                  <div>Buying Price: {{ item.stock.price }}₽</div>
                  <div>Current Price: {{ item.current_price }}₽</div>
                  <div>Changing Percent Price: {{
                      ((item.current_price / item.stock.price * 100) - 100).toFixed(2)
                    }}%
                  </div>
                  <div>Quantity: {{ item.qty }}</div>
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="removeFromPortfolio(item.id)">Remove</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readStocksInPortfolio, readUserProfile} from '@/store/main/getters';
import {dispatchRemoveFromPortfolio} from "@/store/main/actions";

@Component
export default class Dashboard extends Vue {
  public totalPricePortfolio: number = 0;

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }

  get stockPortfolio() {
    const result = readStocksInPortfolio(this.$store);
    for (let item of result) {
      if (item.qty && item.current_price)
        this.totalPricePortfolio += (item.current_price * item.qty);
    }
    return result
  }

  public async removeFromPortfolio(id: number) {
    await dispatchRemoveFromPortfolio(this.$store, id);
  }
}
</script>
