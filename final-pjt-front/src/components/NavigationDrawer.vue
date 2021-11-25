<template>
  <v-navigation-drawer v-model="$store.state.drawer" fixed temporary>
    <v-list-item v-if="isLogin">
      <v-list-item-avatar>
        <img src="https://randomuser.me/api/portraits/women/81.jpg" />
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{ tokenInfo.username }}</v-list-item-title>
        <v-list-item-subtitle>Logged In</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav dense>
      <v-list-item-group
        :value="selected_menu"
        active-class="deep-purple--text text--accent-4"
        mandatory
      >
        <v-list-item
          v-for="item in items"
          :key="item.id"
          link
          @click.prevent="changeRoute(item.route)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>

    <template v-slot:append>
      <div class="pa-2" v-if="!isLogin">
        <v-btn block @click.prevent="changeRoute({ name: 'Registration' })"
          >Registration</v-btn
        >
      </div>
      <div class="pa-2" v-if="!isLogin">
        <v-btn block @click.prevent="changeRoute({ name: 'Login' })"
          >Login</v-btn
        >
      </div>
      <div class="pa-2" v-if="isLogin">
        <v-btn block @click.native="doLogout">Logout</v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "NavigationDrawer",
  data: () => ({
    group: 0,
    items: [
      {
        idx: 0,
        title: "Home",
        icon: "mdi-view-dashboard",
        route: { name: "Home" },
      },
      {
        idx: 1,
        title: "Account",
        icon: "mdi-account",
        route: { name: "Account" },
      },
      {
        idx: 2,
        title: "Community",
        icon: "mdi-forum",
        route: { name: "Community" },
      },
      {
        idx: 3,
        title: "Favorites",
        icon: "mdi-heart",
        route: { name: "Favorites" },
      },
      {
        idx: 4,
        title: "Recommendation",
        icon: "mdi-thumb-up",
        route: { name: "Recommendation" },
      },
    ],
  }),
  methods: {
    ...mapActions(["doLogout", "changeRoute", "setSelectedMenu"]),
  },
  computed: {
    ...mapState(["isLogin", "tokenInfo", "selected_menu"]),
  },
};
</script>

<style></style>
