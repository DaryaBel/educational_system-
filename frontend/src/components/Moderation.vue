<template>
  <div>
    <loader v-if="isLoading"></loader>
    <div v-else>
      <h2>Ваш аккаунт пока не был одобрен Администратором.</h2>
      <p>Ожидайте, обычно это занимает до одного дня.</p>
    </div>
  </div>
</template>
<script>
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "Moderation",
  components: { Loader },
  computed: {
    isLoading() {
      return this.$store.state.isLoading;
    },
  },
};
</script>
