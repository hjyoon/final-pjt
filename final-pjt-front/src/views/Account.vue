<template>
  <v-container>
    <AccountForm></AccountForm>
  </v-container>
</template>

<script>
import AccountForm from "@/components/AccountForm.vue";
import { mapActions } from "vuex";

export default {
  name: "Account",
  components: { AccountForm },
  methods: {
    ...mapActions(["setAppTitle", "setSelectedMenu"]),
  },
  created: function () {
    this.setAppTitle("Home");
    this.setSelectedMenu(1);
  },
};
</script>
