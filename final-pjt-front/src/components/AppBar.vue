<template>
  <v-app-bar app color="primary" dark>
    <v-app-bar-nav-icon @click="setDrawer"></v-app-bar-nav-icon>
    <v-toolbar-title>{{ app_title }}</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "AppBar",
  data: () => ({}),
  methods: {
    ...mapActions(["setDrawer"]),
  },
  computed: {
    ...mapState(["isLogin", "tokenInfo", "app_title", "drawer"]),
  },
};
</script>

<style></style>
