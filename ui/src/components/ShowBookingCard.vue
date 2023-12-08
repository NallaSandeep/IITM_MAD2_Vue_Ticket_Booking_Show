<template>
  <div class="col-md-12">
    <div class="card mb-4 box-shadow">
      <div class="card-body">
        <div class="row">
          <div class="col-md-3 text-truncate">
            <p class="card-text">
              <i class="bi bi-person-fill"></i> {{ bookingCount }}
            </p>
          </div>
          <div class="col-md-3 text-truncate">
            <p class="card-text">
              <i class="bi bi-currency-rupee"></i>
              {{ bookingCount * showPrice }}
            </p>
          </div>
          <div class="col-md-6 text-truncate">
            <p class="card-text">
              <i class="bi bi-at"></i> {{ formattedBookedTime }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import moment from "moment";
export default {
  name: "ShowBookingCard",
  props: {
    userId: Number,
    theatreId: Number,
    theatreName: String,
    theatreArea: String,
    theatreCity: String,
    showName: String,
    showStartTime: String,
    showPrice: Number,
    bookingCount: Number,
    bookedOn: String,
  },
  computed: {
    formattedStartTime() {
      return this.showStartTime == null
        ? null
        : moment(this.showStartTime, "YYYY-MM-DD HH:mm").format(
            "MMMM Do YYYY h:mm A"
          );
    },
    formattedBookedTime() {
      return this.bookedOn == null
        ? null
        : moment(this.bookedOn, "YYYY-MM-DD HH:mm").format(
            "MMMM Do YYYY h:mm A"
          );
    },
  },
};
</script>
