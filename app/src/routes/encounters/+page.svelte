<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	let ssn = '';
	let pid = '';
	let serverLoaded = false;
	/**
	 * @type {string | any[]}
	 */
	let encounters = [];

	onMount(async () => {
		ssn = localStorage.getItem('ssn');
		pid = localStorage.getItem('pid');

		if (!ssn && !pid) {
			goto('/');
		}

		if (ssn && !pid) {
			const res2 = await fetch('http://localhost:8888/patient/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData.reverse();
		}

		if (!ssn && pid) {
			const res2 = await fetch('http://localhost:8888/provider/' + pid + '/encounters');
			const encountersData = await res2.json();
			encounters = encountersData.reverse();
		}
		serverLoaded = true;
	});

	// Use a reactive statement to automatically update the `isLoading` variable

	let filter = '';
	let startDateFilter = '';
	let endDateFilter = '';
	let classFilter = '';

	async function handleFilterChange(event) {
		filter = event.target.value;
	}

	async function handleStartDateFilterChange(event) {
		startDateFilter = event.target.value;
	}

	async function handleClassFilterChange(event) {
		classFilter = event.target.value;
	}
	async function handleEndDateFilterChange(event) {
		endDateFilter = event.target.value;
	}

	async function updateEncounters() {
		serverLoaded = false;
		let url = 'http://localhost:8888/';
		if (!ssn && pid) {
			url += 'provider/' + pid + '/encounters';
		}

		if (startDateFilter) {
			url += `?start=${startDateFilter}`;
		}
		if (endDateFilter) {
			url += `?end=${endDateFilter}`;
		}
		if (classFilter) {
			url += `?class=${classFilter}`;
		}
		console.log(url);
		const res2 = await fetch(url);
		const encountersData = await res2.json();

		encounters = encountersData.reverse();
		serverLoaded = true;
	}

	function clearFilters() {
		filter = '';
		startDateFilter = '';
		endDateFilter = '';
		classFilter = '';
		updateEncounters();
	}

	function toggleMoreInfo(id) {
		const moreInfoElement = document.getElementById(id);
		if (moreInfoElement.hidden) {
			moreInfoElement.hidden = false;
		} else {
			moreInfoElement.hidden = true;
		}
	}
</script>

<button
	class="route-button profile-button"
	on:click={() => {
		goto('/profile');
	}}>My Profile</button
>
<button
	class="route-button logout-button"
	on:click={() => {
		localStorage.removeItem('ssn');
		localStorage.removeItem('pid');
		goto('/');
	}}>Logout</button
>
<div class="container">
	{#if pid && !ssn}
		<div class="left-column">
			<label for="start-date">Start Date</label>
			<input
				id="start-date"
				type="date"
				placeholder="Start Date"
				on:input={handleStartDateFilterChange}
				class="filter-input"
				bind:value={startDateFilter}
			/>
			<label for="end-date">End Date</label>
			<input
				id="end-date"
				type="date"
				placeholder="End Date"
				on:input={handleEndDateFilterChange}
				class="filter-input"
				bind:value={endDateFilter}
			/>
			<label for="class">Class</label>
			<select on:input={handleClassFilterChange} class="filter-input">
				<option value="">All Classes</option>
				<option value="wellness">Wellness</option>
				<option value="emergency">Emergency</option>
				<option value="outpatient">Outpatient</option>
				<option value="inpatient">Inpatient</option>
				<option value="ambulatory">Ambulatory</option>
				<option value="urgentcare">Urgent Care</option>
			</select>

			<button on:click={updateEncounters} class="search-button">Search</button>
			<button on:click={clearFilters} class="clear-button">Clear Filters</button>
		</div>
	{/if}
	<div class="right-column">
		<h1>Encounters</h1>
		{#if !serverLoaded}
			<div class="loading"><h3><i class="fa fa-spinner fa-spin" /> Loading</h3></div>
		{:else if Object.keys(encounters).length > 0 && serverLoaded}
			{#each encounters as encounter}
				{#if pid && !ssn}
					<div class="card">
						<h2>{encounter.description}</h2>
						<p><strong>Start Date:</strong> {new Date(encounter.start).toLocaleString()}</p>
						<p><strong>Stop Date:</strong> {new Date(encounter.stop).toLocaleString()}</p>
						<p><strong>Patient:</strong> {encounter.patient.first} {encounter.patient.last}</p>
						<p><strong>Speciality:</strong> {encounter.provider.speciality}</p>
						<p><strong>Organization:</strong> {encounter.organization.name}</p>
						<p><strong>Address:</strong> {encounter.organization.address}</p>
						<p><strong>Class:</strong> {encounter.encounter_class}</p>
						<button on:click={() => toggleMoreInfo(encounter.id)}>Show More</button>
						<div id={encounter.id} class="more-info" hidden>
							<p><strong>Payer:</strong> {encounter.payer.name}</p>
							{#if encounter.medications.length > 0}
								<p><strong>Medication:</strong></p>
								<ul>
									{#each encounter.medications as medication}
										<li>{medication.description}</li>
									{/each}
								</ul>
							{/if}
							{#if encounter.procedures.length > 0}
								<p><strong>Procedures:</strong></p>
								<ul>
									{#each encounter.procedures as procedure}
										<li>{procedure.description}</li>
									{/each}
								</ul>
							{/if}
							{#if encounter.imaging_studies.length > 0}
								<p><strong>Imaging Studies:</strong></p>
								<ul>
									{#each encounter.imaging_studies as imaging_study}
										<li>{imaging_study.description}</li>
									{/each}
								</ul>
							{/if}
							{#if encounter.devices.length > 0}
								<p><strong>Devices:</strong></p>
								<ul>
									{#each encounter.devices as device}
										<li>{device.description}</li>
									{/each}
								</ul>
							{/if}
							{#if encounter.allergies.length > 0}
								<p><strong>Allergies:</strong></p>
								<ul>
									{#each encounter.allergies as allergy}
										<li>{allergy.description}</li>
									{/each}
								</ul>
							{/if}
							{#if encounter.observations.length > 0}
								<p><strong>Observations:</strong></p>
								<ul>
									{#each encounter.observations as observation}
										<li>{observation.description}</li>
									{/each}
								</ul>
							{/if}
						</div>
					</div>
				{:else}
					<div class="card">
						<h2>{encounter.description}</h2>
						<p><strong>Start Date:</strong> {new Date(encounter.start).toLocaleString()}</p>
						<p><strong>Stop Date:</strong> {new Date(encounter.stop).toLocaleString()}</p>
						<p><strong>Provider:</strong> {encounter.provider.name}</p>
						<p><strong>Speciality:</strong> {encounter.provider.speciality}</p>
						<p><strong>Organization:</strong> {encounter.organization.name}</p>
						<p><strong>Address:</strong> {encounter.organization.address}</p>
						<p><strong>Class:</strong> {encounter.encounter_class}</p>
					</div>
				{/if}
			{/each}
		{:else}
			<div class="card">
				<p>No encounters found.</p>
			</div>
		{/if}
	</div>
</div>

<style>
	h2 {
		font-size: large;
		font-weight: bold;
	}
	.container {
		display: flex;
	}

	.left-column {
		flex-basis: 100px;
		margin-right: 1rem;
		margin-top: 3rem;
	}

	.right-column {
		flex-grow: 2;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.filter-input,
	.search-button,
	.clear-button {
		display: block;
		width: 100%;
		box-sizing: border-box;
		margin-bottom: 10px;
		padding: 5px;
	}

	.search-button,
	.clear-button {
		cursor: pointer;
	}

	.route-button {
		position: absolute;
		top: 20px;
		background-color: rgba(0, 0, 0, 0.7);
		border-radius: 10%;
		color: white;
		padding: 1rem 2rem;
		text-align: center;
		font-size: 1rem;
		cursor: pointer;
	}

	.profile-button {
		right: 10rem;
	}
	.logout-button {
		right: 1rem;
	}
	.fa-spinner {
		font-size: 2rem;
	}
	h3 {
		font-size: 2rem;
	}
	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.more-info {
		margin-top: 10px;
	}
</style>
