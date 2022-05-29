<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Stocks for selling</div>
      </v-card-title>
      <v-card-text>
        <v-container
            fluid
            grid-list-lg
        >
          <v-layout row wrap>
            <v-flex xs12 v-for="stock in stockForSell">
              <v-card>
                <v-card-title primary-title>
                  <div class="headline">Ticker:
                    <a target="_blank"
                       rel="noopener noreferrer"
                       :href="stock.url">
                      {{ stock.ticker }}
                    </a>
                  </div>
                  <v-spacer></v-spacer>
                  <span class="red--text">Price: {{ stock.price }}₽</span>
                </v-card-title>
                <v-card-text>
                  {{ stock.desc }}
                </v-card-text>
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
import {readStocksForSell, readUserProfile} from '@/store/main/getters';

@Component
export default class Dashboard extends Vue {
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


  get stockForSell() {
    return readStocksForSell(this.$store);
  }


}
</script>
