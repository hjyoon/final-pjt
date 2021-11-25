<template>
  <v-container>
    <LoginForm></LoginForm>
  </v-container>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import { mapActions } from "vuex";

export default {
  name: "Login",
  components: { LoginForm },
  methods: {
    ...mapActions(["setAppTitle"]),
  },
  created: function () {
    this.setAppTitle("Login");
  },
};
</script>
