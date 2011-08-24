import commands, os

class BatchJob:
	job_id= None
	user = None
	state = None
	queue = None
	host_from = None
	host_exec = None
	job_name = None
	submit_time = None

	def toString(self):
		return str(self.job_id) + ' ' + str(self.user) + ' ' + str(self.state) + ' ' + str(self.queue) + ' ' + str(self.host_from) + ' ' + str(self.host_exec) + ' ' + str(self.job_name) + ' ' + str(self.submit_time)

class ResourceWatcher:

	def __init__(self, queue, account, group, limit=15, ncpu=44):
		self.queue = queue
		self.account = account
		self.group = group
		self.max_jobs = limit
		self.n_cpu = ncpu

	def nAvailableJobSlots(self):

		nTotalJobs = len(self.listJobsAllAccount())
		# number of submitted jobs fot this account
		nL1CaloJobs = self.nJobsPerAccount(self.account)

		print  nTotalJobs, nL1CaloJobs

		if self.n_cpu==0:
			return self.max_jobs - nL1CaloJobs

		else:
			# number of slots available to account
			# either self.max_jobs or less if others accounts use more slots
			nMaxJobSlots = self.n_cpu - nTotalJobs + nL1CaloJobs
			if nMaxJobSlots > self.max_jobs: nMaxJobSlots=self.max_jobs

			print nMaxJobSlots

			# available slots to send rec jobs
			availableSlots = nMaxJobSlots - nL1CaloJobs
			return availableSlots

	def nJobsPerAccount(self, account):

		cmd = 'bjobs -u ' + account + ' -w | grep -c ' + account
		rawoutput = commands.getoutput(cmd)
		if rawoutput.splitlines()[0]=='No unfinished job found':
			return 0
		else:
			return int(rawoutput)

	def nJobsRunningPerAccount(self, account):

		jobList = self.listJobsPerAccount(account)
		njobs=0
		for job in jobList:
			if job.state=='RUN': njobs=njobs+1
		return njobs


	def nJobsPendingPerAccount(self, account):

		jobList = self.listJobsPerAccount(account)
		njobs=0
		for job in jobList:
			if job.state=='PEND': njobs=njobs+1
		return njobs


	def listJobsAllAccount(self):

		#cmd = 'bjobs -u all  -w | grep ' + self.queue
		cmd = 'bjobs -u ' + self.group + '  -w | grep ' + self.queue
		rawoutput = commands.getoutput(cmd)
		if rawoutput.splitlines()[0]=='No unfinished job found':
			return []
		# no need to skip the first line of the output here
		# JOBID USER STAT QUEUE FROM_HOST EXEC_HOST JOB_NAME SUBMIT_TIME
		jobList = rawoutput.splitlines()

		if jobList == []:
			return []

		batchJobList = []
		for job in jobList:
			parameters = job.split()

			batchJob = BatchJob()
			batchJob.job_id = parameters[0]
			batchJob.user = parameters[1]
			batchJob.state = parameters[2]
			batchJob.queue = parameters[3]
			batchJob.host_from = parameters[4]
			batchJob.host_exec = parameters[5]
			batchJob.job_name = parameters[6]
			batchJob.submit_time = parameters[7]+' '+parameters[8]+' '+parameters[9]

			batchJobList.append(batchJob)

		return batchJobList

	def listJobsPerAccount(self, account):

		cmd = 'bjobs -u ' + account + ' -w'
		rawoutput = commands.getoutput(cmd)
		# skip the first line of the output
		# JOBID USER STAT QUEUE FROM_HOST EXEC_HOST JOB_NAME SUBMIT_TIME
		if rawoutput=='No unfinished job found':
			return []

		jobList = rawoutput.splitlines()[1:]

		batchJobList = []
		for job in jobList:
			parameters = job.split()

			batchJob = BatchJob()
			batchJob.job_id = parameters[0]
			batchJob.user = parameters[1]
			batchJob.state = parameters[2]
			batchJob.queue = parameters[3]
			batchJob.host_from = parameters[4]
			batchJob.host_exec = parameters[5]
			batchJob.job_name = parameters[6]
			batchJob.submit_time = parameters[7]+' '+parameters[8]+' '+parameters[9]

			batchJobList.append(batchJob)

		return batchJobList

	def getJobById(self, jobId):
		cmd = 'bjobs -w ' + str(jobId)
		rawoutput = commands.getoutput(cmd)
		# skip the first line of the output
		# JOBID USER STAT QUEUE FROM_HOST EXEC_HOST JOB_NAME SUBMIT_TIME
		print cmd
		print rawoutput

		if rawoutput.find('not found')!=-1:
			return None

		job = rawoutput.splitlines()[1]
		parameters = job.split()
#		if parameters[0]!= str(jobId):
#			return None
#		else:
		batchJob = BatchJob()
		batchJob.job_id = parameters[0]
		batchJob.user = parameters[1]
		batchJob.state = parameters[2]
		batchJob.queue = parameters[3]
		batchJob.host_from = parameters[4]
		batchJob.host_exec = parameters[5]
		batchJob.job_name = parameters[6]
		batchJob.submit_time = parameters[7]+' '+parameters[8]+' '+parameters[9]
		return batchJob


# bjobs -u larcalib -w
# bjobs -u l1ccalib -w
#  bjobs -u all -w  | grep atlaslarcal


if __name__ == "__main__":

	x = ResourceWatcher('atlasb1','l1ccalib','u_ATLASLARCAL')
	#x = ResourceWatcher('atlaslarcal','l1ccalib')
	#bj = x.listJobsPerAccount('larcalib')
	bj = x.listJobsAllAccount()

	print 'larcalib jobs: '+ str(x.nJobsPerAccount('larcalib'))
	print 'l1ccalib jobs: '+ str(x.nJobsPerAccount('l1ccalib'))
	print 'available slots: ' + str(x.nAvailableJobSlots())

	for y in bj:
		print y.toString() + '\n'
