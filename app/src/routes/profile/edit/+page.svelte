<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { detach_after_dev } from 'svelte/internal';
	let ssn = '';
	let pid = '';
	let patient = {};
	let provider = {};
	let prefix = '';
	let firstName = '';
	let lastName = '';
	let birthdate = '';
	let gender = '';
	let address = '';
	let city = '';
	let state = '';
	let zip = '';
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
			const res = await fetch('http://localhost:8888/patient/' + ssn);
			const { patient: patientData } = await res.json();
			patient = patientData;
			prefix = patient.prefix;
			firstName = patient.first;
			lastName = patient.last;
			birthdate = patient.birthdate;
			ssn = patient.ssn;
			gender = patient.gender;
			address = patient.address;
			city = patient.city;
			state = patient.state;
			zip = patient.zip;

			const res2 = await fetch('http://localhost:8888/patient/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData.slice(-5);
		}

		if (!ssn && pid) {
			const res = await fetch('http://localhost:8888/provider/' + pid);
			const { provider: providerData } = await res.json();
			provider = providerData;

			const res2 = await fetch('http://localhost:8888/provider/' + ssn + '/encounters');
			const { encounters: encountersData } = await res2.json();
			encounters = encountersData.slice(-5);
		}
	});

	// Use a reactive statement to automatically update the `isLoading` variable
	let isLoading = true;
	$: isLoading = Object.keys(provider).length === 0 && Object.keys(patient).length === 0;

	async function updateProfile() {
		try {
			const res = await fetch('http://localhost:8888/patient/' + ssn, {
				method: 'PUT',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					birthdate: birthdate,
					ssn: ssn,
					deathdate: patient.deathdate,
					drivers: patient.drivers,
					passport: patient.passport,
					prefix: prefix,
					first: firstName,
					last: lastName,
					suffix: patient.suffix,
					maiden: patient.maiden,
					marital: patient.marital,
					race: patient.race,
					ethnicity: patient.ethnicity,
					gender: gender,
					birthplace: patient.birthplace,
					address: address,
					city: city,
					state: state,
					county: patient.county,
					fips: patient.fips,
					zip: zip,
					lat: patient.lat,
					lon: patient.lon
				})
			});
		} catch (err) {
			console.log('erro', err);
		}
		console.log(
			JSON.stringify({
				ssn: ssn,
				birthdate: birthdate,
				deathdate: patient.deathdate,
				drivers: patient.drivers,
				passport: patient.passport,
				prefix: prefix,
				first: firstName,
				last: lastName,
				suffix: patient.suffix,
				maiden: patient.maiden,
				marital: patient.marital,
				race: patient.race,
				ethnicity: patient.ethnicity,
				gender: gender,
				birthplace: patient.birthplace,
				address: address,
				city: city,
				state: state,
				county: patient.county,
				fips: patient.fips,
				zip: zip,
				lat: patient.lat,
				lon: patient.lon
			})
		);
	}
</script>

{#if isLoading}
	<h3 class="loading"><i class="fa fa-spinner fa-spin" /> Loading...</h3>
{:else if Object.keys(provider).length > 0}
	<h1>My Provider Profile</h1>
	<div class="cards-container">
		<div class="left-cards">
			<div class="card">
				<h2><i class="fas fa-user" /> Personal Information</h2>
				<p>
					<strong>Name:</strong>
					<label for="prefix">Prefix</label>
					<input type="text" id="prefix" bind:value={prefix} />
				</p>

				<p><strong>Gender:</strong> {provider.gender}</p>
				<p><strong>Speciality:</strong> {provider.speciality}</p>
			</div>
			<div class="card">
				<h2><i class="fas fa-hospital" /> Organization Information</h2>
				<p><strong>Name:</strong> {provider.organization.name}</p>
				<p><strong>Phone:</strong> {provider.organization.phone}</p>
				<p>
					<strong>Address:</strong>
					{provider.organization.address}, {provider.organization.city},
					{provider.organization.state}
					{provider.organization.zip}
				</p>
			</div>
		</div>
	</div>
{:else if Object.keys(patient).length > 0}
	<h1>My Patient Profile</h1>
	<div class="cards-container">
		<div class="left-cards">
			<div class="card">
				<div class="card-header">
					<h2><i class="fas fa-user" /> Personal Information</h2>
				</div>
				<p>
					<strong>Prefix:</strong>
					<input type="text" id="prefix" bind:value={prefix} />
				</p>
				<p>
					<strong>Fisrt Name:</strong>
					<input type="text" id="firstName" bind:value={firstName} />
				</p>
				<p>
					<strong>Last Name:</strong>
					<input type="text" id="lastName" bind:value={lastName} />
				</p>
				<p>
					<strong>Birthdate:</strong>
					<input type="date" id="birthdate" bind:value={birthdate} />
				</p>
				<p>
					<strong>SSN:</strong>
					<input type="text" id="ssn" bind:value={ssn} />
				</p>
				<p>
					<strong>Gender:</strong>
					<input type="text" id="gender" bind:value={gender} />
				</p>
			</div>
			<div class="card">
				<h2><i class="fas fa-map-marker-alt" /> Contact Information</h2>
				<p>
					<strong>Address:</strong>
					<input type="text" id="address" bind:value={address} />
				</p>
				<p>
					<strong>City:</strong>
					<input type="text" id="city" bind:value={city} />
				</p>
				<p>
					<strong>State:</strong>
					<input type="text" id="state" bind:value={state} />
				</p>
				<p>
					<strong>Zip:</strong>
					<input type="text" id="zip" bind:value={zip} />
				</p>
			</div>
			<button type="button" on:click={updateProfile}>Save</button>
		</div>
	</div>
{/if}

<style>
	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.cards-container {
		display: flex;
	}

	.left-cards {
		flex: 1;
		margin-right: 1.5rem;
	}

	.right-card {
		flex: 2;
	}

	.card {
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		width: 100%;
		display: inline-block;
		vertical-align: top;
		margin-bottom: 1rem;
	}

	.card h2 {
		margin: 10px;
		font-size: 1.2rem;
	}

	.card p {
		margin: 10px;
	}

	.fas {
		margin-right: 10px;
	}

	.right-card .card p {
		border: solid thin #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	a {
		color: #000000;
		margin-right: 1rem;
	}
	a:hover {
		color: #000000;
		text-decoration: none;
		cursor: pointer;
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
</style>
