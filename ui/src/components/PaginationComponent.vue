<template>
  <nav>
    <ul class="pagination justify-content-end">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" @click="prevPage" aria-label="Previous"
          >Previous</a
        >
      </li>
      <li
        class="page-item"
        v-for="page in pageCount"
        :key="page"
        :class="{ active: currentPage === page }"
      >
        <a class="page-link" @click="gotoPage(page)">{{ page }}</a>
      </li>
      <li class="page-item" :class="{ disabled: currentPage === pageCount }">
        <a class="page-link" @click="nextPage" aria-label="Next">Next</a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "PaginationComponent",
  props: {
    currentPage: Number,
    pageCount: Number,
  },
  methods: {
    prevPage() {
      if (this.currentPage > 1) {
        this.$emit("page-changed", this.currentPage - 1);
      }
    },
    nextPage() {
      if (this.currentPage < this.pageCount) {
        this.$emit("page-changed", this.currentPage + 1);
      }
    },
    gotoPage(page) {
      this.$emit("page-changed", page);
    },
  },
};
</script>

<style scoped>
/* Add any custom styling for the pagination component here */
</style>
