<template>
  <div>
    <AdminLoggedInHeader v-if="isAdmin" />
    <UserLoggedInHeader v-else-if="isLoggedIn" />
    <LoggedOutHeader v-else />
    <router-view />
  </div>
</template>

<script>
import AdminLoggedInHeader from "./components/AdminLoggedInHeader.vue";
import UserLoggedInHeader from "./components/UserLoggedInHeader.vue";
import LoggedOutHeader from "./components/LoggedOutHeader.vue";
import { mapState, mapMutations } from "vuex";
import { getCookie } from "./util/cookie-util.js";
export default {
  name: "App",
  components: {
    AdminLoggedInHeader,
    UserLoggedInHeader,
    LoggedOutHeader,
  },
  computed: {
    ...mapState(["isLoggedIn"]),
    isAdmin() {
      return this.isLoggedIn && localStorage.isAdmin == "1";
    },
  },
  created() {
    this.setIsLoggedIn(!!getCookie("authToken"));
  },
  watch: {
    isLoggedIn(newValue) {
      if (!newValue) {
        this.setIsLoggedIn(!!getCookie("authToken"));
      }
    },
  },
  methods: {
    ...mapMutations(["setIsLoggedIn"]),
  },
};
</script>

<style>
.text-danger {
  color: #ff5722;
}
</style>
